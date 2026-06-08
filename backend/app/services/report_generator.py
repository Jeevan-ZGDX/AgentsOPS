from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.models.agent import AgentOutput, AgentType, AgentStatus
from app.models.report import Report, ReportType, ReportFormat, ReportStatus


class ReportGeneratorService:
    async def generate(
        self,
        db: AsyncSession,
        project: Project,
        report_type: str = "unified",
        formats: list[str] | None = None,
    ) -> Report:
        if formats is None:
            formats = ["pdf"]

        report = Report(
            project_id=project.id,
            report_type=ReportType(report_type),
            format=ReportFormat(formats[0]),
            status=ReportStatus.GENERATING,
            title=f"{project.name} - {report_type.replace('_', ' ').title()} Report",
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)

        from app.workers.celery_app import generate_report_task
        generate_report_task.delay(
            project_id=project.id,
            report_id=report.id,
            report_type=report_type,
            formats=formats,
        )

        return report

    async def export(
        self,
        db: AsyncSession,
        project: Project,
        report_type: str = "unified",
        export_format: str = "pdf",
    ) -> dict:
        report = await self.generate(db, project, report_type, [export_format])
        return {
            "report_id": report.id,
            "status": "generating",
            "message": f"Report will be available for download shortly",
        }
