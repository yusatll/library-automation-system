from celery import Celery
from celery.schedules import crontab

# Görev kuyruğu için bir Celery uygulaması oluşturun
celery_app = Celery('library_tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

# Görevlerin hangi kuyruğa yönlendirileceğini yapılandırın
celery_app.conf.task_routes = {
    'celery_app.tasks.send_overdue_reminders': {'queue': 'reminders'},
    'celery_app.tasks.generate_weekly_report': {'queue': 'reports'},
}

celery_app.conf.beat_schedule = {
    'send-daily-overdue-reminders': {
        'task': 'celery_app.tasks.send_overdue_reminders',
        'schedule': crontab(hour=9, minute=0),  # Her gün sabah 9:00'da çalıştır
    },
    'generate-weekly-report': {
        'task': 'celery_app.tasks.generate_weekly_report',
        'schedule': crontab(day_of_week=0, hour=0, minute=0),  # Her pazar gece yarısı çalıştır
    },
}

celery_app.conf.timezone = 'UTC'

# Optional: Configure Celery to use SQLAlchemy sessions
from app.dependencies import SessionLocal

@celery_app.on_task_init.connect
def init_celery_task(sender, **kwargs):
    with SessionLocal() as session:
        sender.app.task_session = session