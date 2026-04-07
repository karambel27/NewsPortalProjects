from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        """
        Обновляет рейтинг автора исходя из трех составляющих:
        1. Суммы оценок статей, умноженная на 3.
        2. Суммы оценок собственных комментариев.
        3. Суммы оценок комментариев под своими статьями.
        """
        summ_article = sum([posts.rating for posts in Post.objects.filter(author=self, type='article')]) * 3
        summ_comments = sum([comments.rating for comments in Comment.objects.filter(user=self.user)])
        summ_author = sum(
            [comments.rating for comments in Comment.objects.filter(post__author=self, post__type='article')])
        self.rating = summ_article + summ_comments + summ_author
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


POST_TYPES = (
    ('article', 'Статья'),
    ('news', 'Новость')
)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    type = models.CharField(max_length=7, choices=POST_TYPES, verbose_name='Тип поста')
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', blank=True, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')

    def get_absolute_url(self):
        return reverse('new' if self.type == 'news' else 'article', kwargs={'pk': self.pk})

    def preview(self):
        return self.content[:124] + "..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating >= 1:
            self.rating -= 1
            self.save()

    def __str__(self):
        return f'{self.title}: {self.preview()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating >= 1:
            self.rating -= 1
            self.save()
