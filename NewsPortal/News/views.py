from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models


def index(requests):
    posts = models.Post.objects.all().order_by('-created_at')
    data = {
        'title': 'Главная страница',
        'posts': posts,
        'length_post': f'Количество новостей: {models.Post.objects.filter(type='news').count()} '
                       f'Количество статей: {models.Post.objects.filter(type='article').count()}'}
    return render(requests, 'News/index.html', data)


class NewsList(ListView):
    model = models.Post
    queryset = models.Post.objects.filter(type='news')

    ordering = '-created_at'
    template_name = 'News/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Список новостей'
        context['length_post'] = f'Количество новостей: {self.queryset.count()} '
        return context


class ArticleList(ListView):
    model = models.Post
    queryset = models.Post.objects.filter(type='article')

    ordering = '-created_at'
    template_name = 'News/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Список статей'
        context['length_post'] = f'Количество статей: {self.queryset.count()} '

        return context


class PostList(DetailView):
    model = models.Post
    template_name = 'News/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        dic = {'news':'Новость', 'article':'Статья'}
        context['title'] = f'{dic[self.object.type]}: {self.object.title}'
        return context

