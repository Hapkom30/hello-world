import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from datetime import datetime, timedelta

from NewsLents2.models import Post

logger = logging.getLogger(__name__)


def my_job():
    date_now = datetime.now()
    date_old = date_now - timedelta(days=7)
    post_list = Post.objects.filter(date__range=(date_old, date_now))
    users = User.objects.exclude(email='')

    text = ''
    text_html = ''
    subject = f'Список последних новостей за неделю:'
    i = 0

    for p in post_list:
        i += 1
        text += f'{i}.{p.title} http://127.0.0.1:8000{p.get_absolute_url()}\n'
        text_html += f'''{i}.<b><a href='http://127.0.0.1:8000{p.get_absolute_url()}'>{p.title}</a></b>\n'''

    for user in users:
        msg = EmailMultiAlternatives(subject, text, None, [user.email])
        msg.attach_alternative(text_html, "text/html")
        msg.send()



@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', minute="18", hour="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")