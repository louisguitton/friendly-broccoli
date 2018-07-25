from celery.utils.log import get_task_logger
from app import celery

logger = get_task_logger(__name__)


@celery.task
def print_hello():
    logger.info("Hello")
