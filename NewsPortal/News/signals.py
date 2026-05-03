from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal import settings
from .models import Post, Category


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add' and instance.type == 'article':
        post = instance
        added_categories = Category.objects.filter(pk__in=pk_set)
        for category in added_categories:
            subscribers = category.subscribers.all()
            if subscribers.exists():
                article_link = post.get_absolute_url()
                subject = f"Новая статья в категории '{category.name}': {post.title}"
                message = render_to_string('new_article_notification.html',
                                           {'post': post, 'link': article_link, 'name': category.name})
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [subscriber.email for subscriber in subscribers]
                send_mail(subject, message, from_email, recipient_list, html_message=message)


'''Если пользователь подписан на какую-либо категорию, то, как только в неё добавляется новая статья, 
её краткое содержание приходит пользователю на электронную почту, которую он указал при регистрации. 
В письме обязательно должна быть гиперссылка на саму статью, чтобы он мог 
по клику перейти и прочитать её.'''
