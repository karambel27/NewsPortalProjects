from datetime import datetime
import string
from django import template

register = template.Library()


@register.filter()
def current_time(value, format_string='%d-%m-%Y'):
    return value.strftime(format_string)


@register.filter(name='censor')
def censor_text(value):
    # Проверка типа данных
    if not isinstance(value, str):
        raise TypeError(f"Ожидается строка, получено {type(value).__name__}")
    bad_words = ['козел', 'корова', 'урод', 'дурак', 'дура', 'штемп', 'редиска', 'плохой', 'нехороший']

    parts = []
    current_word = ''

    # Разбиваем строку на слова и знаки
    for char in value:
        if char.isalpha():
            current_word += char
        else:
            if current_word:
                # Если накопилось слово, добавляем его в список
                parts.append(current_word)
                current_word = ''
            parts.append(char)

    parts.append(current_word)

    word_list = [word if word.lower() not in bad_words else word[0] + '*' * (len(word) - 1) for word in
                 parts]

    return ''.join(word_list)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
