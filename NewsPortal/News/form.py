from django import forms

from .models import Post, Category, Author


class FormAddpost(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False,
                                                label="Категория")
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    empty_label='Автор не выбран', label="Автор")

    class Meta:
        model = Post
        fields = ['author', 'title', 'content',
                  'categories']

