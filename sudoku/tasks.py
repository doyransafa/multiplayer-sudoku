from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Room
from datetime import datetime, timedelta
from app.celery import app
from celery.schedules import crontab

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
  return x + y


@shared_task
def bos():
  return


@shared_task
def xsum(numbers):
  return sum(numbers)


@app.task
def delete_old_rooms():
  time_treshold = datetime.now() - timedelta(minutes=1)
  old_rooms = Room.objects.filter(created_at__time__lt=time_treshold)
  old_rooms.delete()
  logger.info(f'{old_rooms.count()} rooms deleted!')

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
  
  sender.add_periodic_task(crontab(minute="*/1"), delete_old_rooms.s(), name='Delete rooms older than a minute')

  # sender.add_periodic_task(timedelta(second=30), add.s(2,3), name='add 3 to 2 every 30 seconds')

