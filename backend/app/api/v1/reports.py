from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.project import Project
from app.models.report import Report
from app.schemas.report import ReportResponse, ReportListResponse, GenerateReportRequest, ExportRequest
from app.services.report_generator import ReportGeneratorService

router = APIRouter()


@router.get("/{project_id}", response_model=ReportListResponse)
async def get_reports(
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

    reports_result = await db.execute(
        select(Report)
        .where(Report.project_id == project_id)
        .order_by(desc(Report.created_at))
    )
    items = reports_result.scalars().all()

    return ReportListResponse(
        items=[ReportResponse.model_validate(r) for r in items],
        total=len(items),
    )


@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_report(
    request: GenerateReportRequest,
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

    generator = ReportGeneratorService()
    report = await generator.generate(db, project, request.report_type, request.formats)

    return {"report_id": report.id, "status": "generating"}


@router.get("/{project_id}/{report_id}", response_model=ReportResponse)
async def get_report(
    project_id: int,
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Report).where(
            Report.id == report_id,
            Report.project_id == project_id,
        )
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.post("/export")
async def export_report(
    request: ExportRequest,
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

    generator = ReportGeneratorService()
    return await generator.export(db, project, request.report_type, request.format)
