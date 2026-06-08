from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "agentops",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.workers.tasks.agent_tasks",
        "app.workers.tasks.report_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,
    task_soft_time_limit=300,
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
)
