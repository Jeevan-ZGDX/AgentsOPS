from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.agent import AgentOutput, AgentStatus
from app.models.report import Report
from app.schemas.dashboard import DashboardOverviewResponse, AnalyticsResponse

router = APIRouter()


@router.get("/overview", response_model=DashboardOverviewResponse)
async def dashboard_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    total = await db.execute(
        select(func.count()).select_from(Project).where(Project.owner_id == current_user.id)
    )
    total_projects = total.scalar()

    active = await db.execute(
        select(func.count()).select_from(Project).where(
            Project.owner_id == current_user.id,
            Project.status == ProjectStatus.IN_PROGRESS,
        )
    )
    active_projects = active.scalar()

    completed = await db.execute(
        select(func.count()).select_from(Project).where(
            Project.owner_id == current_user.id,
            Project.status == ProjectStatus.COMPLETED,
        )
    )
    completed_projects = completed.scalar()

    reports_count = await db.execute(
        select(func.count()).select_from(Report).where(
            Report.project_id.in_(
                select(Project.id).where(Project.owner_id == current_user.id)
            )
        )
    )
    total_reports = reports_count.scalar()

    avg_viability = await db.execute(
        select(func.avg(Project.viability_score)).where(
            Project.owner_id == current_user.id,
            Project.viability_score.isnot(None),
        )
    )
    avg_v = avg_viability.scalar()

    avg_readiness = await db.execute(
        select(func.avg(Project.investor_readiness_score)).where(
            Project.owner_id == current_user.id,
            Project.investor_readiness_score.isnot(None),
        )
    )
    avg_r = avg_readiness.scalar()

    recent_projects_result = await db.execute(
        select(Project)
        .where(Project.owner_id == current_user.id)
        .order_by(desc(Project.created_at))
        .limit(5)
    )
    recent_projects = [
        {
            "id": p.id,
            "name": p.name,
            "industry": p.industry,
            "status": p.status.value,
            "created_at": p.created_at.isoformat(),
        }
        for p in recent_projects_result.scalars().all()
    ]

    return DashboardOverviewResponse(
        total_projects=total_projects,
        active_projects=active_projects,
        completed_projects=completed_projects,
        total_reports=total_reports,
        avg_viability_score=float(avg_v) if avg_v else None,
        avg_investor_readiness=float(avg_r) if avg_r else None,
        recent_projects=recent_projects,
        recent_activity=[],
    )


@router.get("/analytics", response_model=AnalyticsResponse)
async def dashboard_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    projects_by_status = {}
    for status_enum in ProjectStatus:
        count = await db.execute(
            select(func.count()).select_from(Project).where(
                Project.owner_id == current_user.id,
                Project.status == status_enum,
            )
        )
        projects_by_status[status_enum.value] = count.scalar()

    projects_by_industry_result = await db.execute(
        select(Project.industry, func.count())
        .where(Project.owner_id == current_user.id)
        .group_by(Project.industry)
    )
    projects_by_industry = dict(projects_by_industry_result.all())

    projects_by_model_result = await db.execute(
        select(Project.business_model, func.count())
        .where(Project.owner_id == current_user.id)
        .group_by(Project.business_model)
    )
    projects_by_business_model = dict(projects_by_model_result.all())

    agent_times_result = await db.execute(
        select(
            AgentOutput.agent_type,
            func.avg(AgentOutput.execution_time_ms),
        )
        .where(
            AgentOutput.project_id.in_(
                select(Project.id).where(Project.owner_id == current_user.id)
            ),
            AgentOutput.status == AgentStatus.COMPLETED,
        )
        .group_by(AgentOutput.agent_type)
    )
    agent_execution_times = {str(k): float(v) for k, v in agent_times_result.all() if v}

    agent_success_result = await db.execute(
        select(
            AgentOutput.agent_type,
            func.count().filter(AgentOutput.status == AgentStatus.COMPLETED),
            func.count(),
        )
        .where(
            AgentOutput.project_id.in_(
                select(Project.id).where(Project.owner_id == current_user.id)
            ),
        )
        .group_by(AgentOutput.agent_type)
    )
    agent_success_rates = {}
    for row in agent_success_result.all():
        agent_type, completed, total_count = row
        agent_success_rates[str(agent_type)] = (completed / total_count * 100) if total_count > 0 else 0

    return AnalyticsResponse(
        projects_by_status=projects_by_status,
        projects_by_industry=projects_by_industry,
        projects_by_business_model=projects_by_business_model,
        agent_execution_times=agent_execution_times,
        agent_success_rates=agent_success_rates,
        scores_over_time=[],
        usage_stats={},
    )
