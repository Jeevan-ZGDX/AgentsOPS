import time
import json
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import get_settings
from app.workers.celery_app import celery_app
from app.models.agent import AgentOutput, AgentType, AgentStatus
from app.models.project import Project, ProjectStatus
from app.ai.orchestrator.workflow import AgentOpsWorkflow

settings = get_settings()

sync_engine = create_engine(
    settings.DATABASE_URL.replace("+asyncpg", "+psycopg2"),
    pool_size=5,
    max_overflow=10,
)
SyncSessionLocal = sessionmaker(bind=sync_engine)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def execute_agent_workflow(self, project_id: int, execution_id: str, agent_types: list[str]):
    db = SyncSessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "Project not found", "project_id": project_id}

        workflow = AgentOpsWorkflow()
        result = workflow.run(
            project_id=project_id,
            project_data={
                "name": project.name,
                "industry": project.industry,
                "problem_statement": project.problem_statement,
                "solution": project.solution,
                "target_audience": project.target_audience,
                "business_model": project.business_model.value if hasattr(project.business_model, 'value') else project.business_model,
                "country": project.country,
            },
            agent_types=agent_types,
        )

        for agent_result in result.get("agent_outputs", []):
            agent_type = agent_result["agent_type"]
            db_agent = db.query(AgentOutput).filter(
                AgentOutput.project_id == project_id,
                AgentOutput.agent_type == AgentType(agent_type),
            ).first()
            if db_agent:
                db_agent.status = AgentStatus.COMPLETED
                db_agent.output_data = agent_result.get("output", {})
                db_agent.execution_time_ms = agent_result.get("execution_time_ms")
                db_agent.token_usage = agent_result.get("token_usage", {})
                db_agent.cost_usd = agent_result.get("cost_usd")
                db_agent.completed_at = datetime.utcnow()

        project.status = ProjectStatus.COMPLETED
        project.viability_score = result.get("viability_score")
        project.investor_readiness_score = result.get("investor_readiness_score")
        project.completed_at = datetime.utcnow()
        db.commit()

        return {
            "execution_id": execution_id,
            "project_id": project_id,
            "status": "completed",
            "result": result,
        }

    except Exception as exc:
        db.rollback()
        agent_outputs = db.query(AgentOutput).filter(
            AgentOutput.project_id == project_id,
            AgentOutput.status == AgentStatus.RUNNING,
        ).all()
        for ao in agent_outputs:
            ao.status = AgentStatus.FAILED
            ao.error_message = str(exc)
            ao.completed_at = datetime.utcnow()
        db.commit()

        try:
            self.retry(exc=exc)
        except Exception:
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.FAILED
                db.commit()
            return {"error": str(exc), "project_id": project_id}

    finally:
        db.close()
