import os

from celery import Celery

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "medical_rag",
    broker=redis_url,
    backend=redis_url,
    include=[
        "app.jobs.document_tasks",
        "app.jobs.evaluation_tasks",
    ],
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=1800,
    task_soft_time_limit=1740,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
import os

from celery import Celery

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "medical_rag",
    broker=redis_url,
    backend=redis_url,
    include=[
        "app.jobs.document_tasks",
        "app.jobs.evaluation_tasks",
    ],
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=1800,
    task_soft_time_limit=1740,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
import os

from celery import Celery

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "medical_rag",
    broker=redis_url,
    backend=redis_url,
    include=[
        "app.jobs.document_tasks",
        "app.jobs.evaluation_tasks",
    ],
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=int(os.environ.get("CELERY_TASK_TIME_LIMIT", 1800)),
    task_soft_time_limit=int(os.environ.get("CELERY_TASK_SOFT_TIME_LIMIT", 1740)),
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
