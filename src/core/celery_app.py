from celery import Celery
from src.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "plt",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Import task modules here (placeholder for future task imports)
# celery_app.autodiscover_tasks(["src.tasks"])
