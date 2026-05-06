from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from . import models
from .form import FormAddpost
from .models import Post, Category
from .utils import PostTypeValidationMixin
from .filters import PostsFilter


class IndexView(ListView):
    # def get(self, request):
    #     weekly_newsletter.delay()
    #     return HttpResponse('Hello!')

    model = Post
    template_name = 'News/index.html'
    ordering = '-created_at'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница'}
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        context['length_post'] = (f'Количество новостей: {self.get_queryset().filter(type='news').count()} '
                                  f'Количество статей: {self.get_queryset().filter(type='article').count()}')
        context['num_post'] = len(self.filterset.qs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostsList(ListView):
    model = models.Post
    template_name = 'News/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        context['num_post'] = len(self.filterset.qs)
        context['title'] = 'Список новостей' if self.post_type == 'news' else 'Список статей'
        type_name = 'новостей' if self.post_type == 'news' else 'статей'
        context['length_post'] = f'Количество {type_name}: {self.get_queryset().count()}'
        return context

    def get_queryset(self):
        self.post_type = self.kwargs.get('post_type')
        self.filterset = PostsFilter(self.request.GET, Post.objects.filter(type=self.post_type).order_by('-created_at'))
        return self.filterset.qs


class ShowPost(PostTypeValidationMixin, DetailView):
    model = models.Post
    template_name = 'News/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        dic = {'news': 'Новость', 'article': 'Статья'}
        context['edit_prov'] = self.request.user == self.get_object().author.user or self.request.user.is_superuser
        context['title'] = f'{dic[self.object.type]}: {self.object.title}'
        return context


class AddPost(PermissionRequiredMixin, CreateView):
    model = Post
    # success_url = reverse_lazy('home')
    form_class = FormAddpost
    template_name = 'News/add_post.html'
    permission_required = 'News.add_post'

    def form_valid(self, form):
        post_type = self.kwargs.get('post_type')
        form.instance.type = post_type
        w = form.save(commit=False)
        w.author = self.request.user.author
        # msg = EmailMultiAlternatives('Проверка',
        #                              'Базовое сообщение',
        #                              'panovdaniil201510@yandex.ru',
        #                              ['panovdaniil2015@list.ru', ])
        # html_content = render_to_string('soobshenie.html', {'w': w})
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        # send_mail('Проверка', 'Это базовое сообщение', 'panovdaniil201510@yandex.ru',
        #           ['ts78@list.ru', 'panovdaniil2015@list.ru'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dic = {'news': 'новостей', 'article': 'статьи'}
        context['title'] = 'Добавление ' + dic[self.kwargs.get('post_type')]
        return context


class UpdatePost(PostTypeValidationMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'News/add_post.html'
    # success_url = reverse_lazy('home')
    fields = ['author', 'title', 'content',
              'categories']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dic = {'news': 'новостей', 'article': 'статьи'}
        context['title'] = 'Редактирование ' + dic[self.kwargs.get('post_type')]
        return context


class DeletePost(PostTypeValidationMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'News/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'({self.object.title}): Удаление'
        return context


class CategoriesView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'News/categories_view.html'
    context_object_name = 'categories'
    extra_context = {'title': 'Категории'}


@login_required
def subscribe_ot(request, pk):
    cat = Category.objects.get(pk=pk)
    user = request.user
    if cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.remove(user)
    else:
        cat.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))

# def index(requests):
#     posts = models.Post.objects.all().order_by('-created_at')
#     data = {
#         'title': 'Главная страница',
#         'posts': posts,
#         'length_post': f'Количество новостей: {models.Post.objects.filter(type='news').count()} '
#                        f'Количество статей: {models.Post.objects.filter(type='article').count()}'}
#     return render(requests, 'News/index.html', data)
