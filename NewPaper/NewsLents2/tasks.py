from celery import shared_task
from django.core.mail import EmailMultiAlternatives
import time

from django.contrib.auth.models import User
from NewsLents2.models import Post

from datetime import datetime, timedelta



@shared_task
def send_notification(title, msg, msg_html, email):
    time.sleep(5)
    msg = EmailMultiAlternatives(title, msg, None, [email])
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
    print(F'message sended  in {email}')

@shared_task
def newsletter_task():
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