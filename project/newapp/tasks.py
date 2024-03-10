# импортируем декоратор из библиотеки
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post
from django.conf import settings


@shared_task  # рассылка уведомлений на email подписчиков при создании новости подписанной категории
def send_email_task(pk):
    post = Post.objects.get(pk=pk)  # определяем созданную новость по pk
    title = post.title  # определяем заголовок созданной новости

    subscribers_emails = User.objects.filter(subscriptions__category__in=post.postCategory.all()).values_list('email',flat=True)

    html_content = render_to_string(
        'news_created_email_task.html',
        {
            f'Title: {post.title}',
            f'Text: {post.preview()}',
            f'URL: {settings.SITE_URL}/news/{pk}',
        }
    )

    for email in subscribers_emails:
        msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
