# commands/runapscheduler.py
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from NewsPortal import settings
from News.tasks import weekly_newsletter


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запускает планировщик APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу еженедельной рассылки
        scheduler.add_job(
            weekly_newsletter,
            trigger=CronTrigger(day_of_week="sun", hour=14, minute=28),  # Каждое воскресенье в 10:00
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )

        # Запуск планировщика
        try:
            self.stdout.write("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write("Остановка планировщика...")
            scheduler.shutdown()
            self.stdout.write("Планировщик остановлен успешно!")
