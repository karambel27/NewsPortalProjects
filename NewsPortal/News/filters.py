from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter, ModelChoiceFilter
from .models import Post, Author, Category

from django import forms


class PostsFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название',
    )

    # author_username = CharFilter(
    #     field_name='author__user__username',
    #     lookup_expr='exact',
    #     label='Автор'
    # )

    author_username = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        to_field_name='id',
        label='Автор',
        empty_label="--- Выберите автора ---", )

    categories = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id',
        label="Категория",
        empty_label='--- Выбрать категорию ---'
    )

    created_after = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата (позже)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['author_username', 'title', "categories", 'created_after']
