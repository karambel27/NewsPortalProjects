from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models
from .models import Post


class IndexView(ListView):
    template_name = 'News/index.html'
    queryset = Post.objects.all().order_by('-created_at')
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'length_post': f'Количество новостей: {models.Post.objects.filter(type='news').count()} '
                       f'Количество статей: {models.Post.objects.filter(type='article').count()}'}


class PostsList(ListView):
    model = models.Post
    template_name = 'News/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Список новостей' if self.post_type == 'news' else 'Список статей'
        type_name = 'новостей' if self.post_type == 'news' else 'статей'
        context['length_post'] = f'Количество {type_name}: {self.get_queryset().count()}'
        return context

    def get_queryset(self):
        self.post_type = self.kwargs.get('post_type')
        return Post.objects.filter(type=self.post_type).order_by('-created_at')


class ShowPost(DetailView):
    model = models.Post
    template_name = 'News/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        dic = {'news': 'Новость', 'article': 'Статья'}
        context['title'] = f'{dic[self.object.type]}: {self.object.title}'
        return context

# def index(requests):
#     posts = models.Post.objects.all().order_by('-created_at')
#     data = {
#         'title': 'Главная страница',
#         'posts': posts,
#         'length_post': f'Количество новостей: {models.Post.objects.filter(type='news').count()} '
#                        f'Количество статей: {models.Post.objects.filter(type='article').count()}'}
#     return render(requests, 'News/index.html', data)
