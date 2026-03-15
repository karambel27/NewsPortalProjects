from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


POST_TYPES = (
    ('article', 'Статья'),
    ('news', 'Новость')
)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory',
                                        related_name='cat')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.FloatField(default=0.0)

    def preview(self):
        return self.content[:124]+"..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating >= 1:
            self.rating -= 1
            self.save()


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


"""Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
Метод update_rating() модели Author, который обновляет рейтинг текущего автора (метод принимает в качестве аргумента только self).
Он состоит из следующего:
суммарный рейтинг каждой статьи автора умножается на 3;
суммарный рейтинг всех комментариев автора;
суммарный рейтинг всех комментариев к статьям автора."""
