from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import PostCategory
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, action, **kwargs):

    if action == 'post_add':

        category_post = instance.category.all()
        emails: list[str] = []
        for category in category_post:
            emails += category.subscribers.all()

        emails = [s.email for s in emails]


        subject = f'Дорогой друг, спеши прочесть новую новость из категории на которую ты подписан!!!'

        text_content = (
            f'{instance.title}\n'
            f'{instance.preview()}\n\n'
            f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'{instance.title}<br>'
            f'{instance.preview()}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на новость</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()