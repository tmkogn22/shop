import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')


app = Celery('shop')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


app.conf.beat_schedule = {
    'example': {
        'task': 'catalog.tasks.example_schedule_task',
        'schedule': crontab(minute='*/2')
    },
    'check_orders': {
        'task': 'catalog.tasks.check_paid_orders',
        'schedule': crontab(minute='*/2')
    },
    'broadcast_discount_info': {
        'task': 'catalog.tasks.broadcast_discount_info',
        'schedule': crontab(minute='*/2')
    }

}
