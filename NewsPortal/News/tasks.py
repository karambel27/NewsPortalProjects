import time

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from NewsPortal import settings
from .models import Post, Category


@shared_task
def weekly_newsletter():
    now = timezone.now()
    week_ago = now - timezone.timedelta(days=7)
    new_articles = Post.objects.filter(created_at__gte=week_ago, type='news')
    for user in get_user_model().objects.all():
        subscribed_categories = user.categories.all()
        if subscribed_categories.exists():
            user_articles = new_articles.filter(categories__in=subscribed_categories).distinct()

            if user_articles.exists():
                subject = "Новые новости за неделю"
                message = render_to_string('weekly_newsletter.html', {'articles': user_articles})
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list, html_message=message)


"""Если пользователь подписан на какую-либо категорию, то каждую неделю ему 
приходит на почту список новых статей, появившийся за неделю с гиперссылкой 
на них, чтобы пользователь мог перейти и прочесть любую из статей."""


@shared_task
def notify_subscribers_task(pk, post_id):
    added_categories = Category.objects.filter(pk__in=pk)
    post = Post.objects.get(pk=post_id)
    for category in added_categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            article_link = post.get_absolute_url()
            subject = f"Новая новость в категории '{category.name}': {post.title}"
            message = render_to_string('new_article_notification.html',
                                       {'post': post, 'link': article_link, 'name': category.name})
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [subscriber.email for subscriber in subscribers]
            send_mail(subject, message, from_email, recipient_list, html_message=message)

