import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project, ProjectStatus, ProjectState
from app.models.agent import AgentOutput, AgentType, AgentStatus


class AgentOrchestratorService:
    async def start_execution(
        self,
        db: AsyncSession,
        project: Project,
        agent_types: list[str],
    ) -> str:
        execution_id = str(uuid.uuid4())

        project.status = ProjectStatus.IN_PROGRESS
        await db.commit()

        state = ProjectState(
            project_id=project.id,
            state_data={"status": ProjectStatus.IN_PROGRESS.value, "execution_id": execution_id},
            version=2,
            description="Agent execution started",
        )
        db.add(state)

        for agent_type_str in agent_types:
            agent_type = AgentType(agent_type_str)
            agent_output = AgentOutput(
                project_id=project.id,
                agent_type=agent_type,
                status=AgentStatus.PENDING,
                input_data={
                    "execution_id": execution_id,
                    "project_id": project.id,
                    "agent_type": agent_type.value,
                    "project_data": {
                        "name": project.name,
                        "industry": project.industry,
                        "problem_statement": project.problem_statement,
                        "solution": project.solution,
                        "target_audience": project.target_audience,
                        "business_model": project.business_model.value if hasattr(project.business_model, 'value') else project.business_model,
                        "country": project.country,
                    },
                },
            )
            db.add(agent_output)

        await db.commit()

        from app.workers.celery_app import execute_agent_workflow
        execute_agent_workflow.delay(
            project_id=project.id,
            execution_id=execution_id,
            agent_types=agent_types,
        )

        return execution_id
