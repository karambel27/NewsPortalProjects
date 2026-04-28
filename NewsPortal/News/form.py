from django import forms
from allauth.account.forms import SignupForm
from .models import Post, Category


class FormAddpost(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False,
                                                label="Категория")

    # author = forms.ModelChoiceField(queryset=Author.objects.all(),
    #                                 empty_label='Автор не выбран', label="Автор")

    class Meta:
        model = Post
        fields = ['title', 'content',
                  'categories']
