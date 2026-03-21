from datetime import datetime
import string
from django import template


register = template.Library()


@register.filter()
def current_time(value, format_string='%d-%m-%Y'):
   return value.strftime(format_string)

@register.filter()
def censor(value):
   bad_words = ['козел','корова', 'урод', 'дурак', 'дура', 'штемп', 'мразь']
   value_list = [word if word.lower() not in bad_words else word[0] + '*' * (len(word) - 1) for word in value.split(' ')]
   return ' '.join(value_list)
