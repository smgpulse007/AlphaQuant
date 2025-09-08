import os
from celery import Celery


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "alpha",
    broker=REDIS_URL,
    backend=REDIS_URL,
)


@celery.task(name="alpha.run")
def alpha_run(payload: dict):
    from src.orchestrator.graph import app as graph
    return graph.run(payload)

