from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal import settings
from .models import Post, Category
from .tasks import notify_subscribers_task


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add' and instance.type == 'news':
        post_id = instance.id
        pk = list(pk_set)
        notify_subscribers_task.delay(pk, post_id)


'''Если пользователь подписан на какую-либо категорию, то, как только в неё добавляется новая статья, 
её краткое содержание приходит пользователю на электронную почту, которую он указал при регистрации. 
В письме обязательно должна быть гиперссылка на саму статью, чтобы он мог 
по клику перейти и прочитать её.'''
