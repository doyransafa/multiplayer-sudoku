from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Room
from datetime import datetime, timedelta
from app.celery import app
from celery.schedules import crontab

logger = get_task_logger(__name__)


@app.task
def add(x, y):
  logger.info('Added numbers')
  return x + y


@shared_task
def bos():
  return


@shared_task
def delete_room_after_24_hours(room_code):
  try:
    room = Room.objects.get(id=room_code)
    room.delete()
    logger.info('DELETED ROOOM')
  except Room.DoesNotExist:
    logger.info('NO ROOOM')
