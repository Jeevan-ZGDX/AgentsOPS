from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.project import Project
from app.models.agent import AgentOutput, AgentType, AgentStatus
from app.schemas.agent import RunAgentRequest, AgentOutputResponse, AgentStatusResponse
from app.services.orchestrator import AgentOrchestratorService

router = APIRouter()


@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
async def run_agents(
    request: RunAgentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Project).where(
            Project.id == request.project_id,
            Project.owner_id == current_user.id,
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    orchestrator = AgentOrchestratorService()
    execution_id = await orchestrator.start_execution(db, project, request.agent_types)

    return {"execution_id": execution_id, "status": "started", "project_id": request.project_id}


@router.get("/status/{project_id}", response_model=AgentStatusResponse)
async def get_agent_status(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    agents_result = await db.execute(
        select(AgentOutput)
        .where(AgentOutput.project_id == project_id)
        .order_by(AgentOutput.created_at)
    )
    agents = agents_result.scalars().all()

    if not agents:
        return AgentStatusResponse(
            project_id=project_id,
            agents=[],
            overall_status="not_started",
            progress_percentage=0.0,
        )

    completed = sum(1 for a in agents if a.status == AgentStatus.COMPLETED)
    total = len(agents)
    statuses = [a.status.value for a in agents]

    if AgentStatus.FAILED.value in statuses:
        overall = "failed"
    elif all(s == AgentStatus.COMPLETED.value for s in statuses):
        overall = "completed"
    elif any(s == AgentStatus.RUNNING.value for s in statuses):
        overall = "running"
    else:
        overall = "pending"

    return AgentStatusResponse(
        project_id=project_id,
        agents=[AgentOutputResponse.model_validate(a) for a in agents],
        overall_status=overall,
        progress_percentage=(completed / total * 100) if total > 0 else 0,
    )


@router.get("/output/{project_id}", response_model=list[AgentOutputResponse])
async def get_agent_outputs(
    project_id: int,
    agent_type: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    query = select(AgentOutput).where(AgentOutput.project_id == project_id)
    if agent_type:
        query = query.where(AgentOutput.agent_type == agent_type)
    query = query.order_by(AgentOutput.created_at)

    agents_result = await db.execute(query)
    return agents_result.scalars().all()
