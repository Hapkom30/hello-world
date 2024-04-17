from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import PostCategory
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Дорогой друг, спеши прочесть новую новость из категории на которую ты подписан!!! {instance.category}'

    text_content = (
        f'{instance.post.title}\n'
        f'{instance.post.preview()}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'{instance.post.title}<br>'
        f'{instance.post.preview()}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()