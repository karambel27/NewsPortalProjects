# mixins.py
from django.http import Http404


class PostTypeValidationMixin:
    """
    Миксин для проверки соответствия типа поста из URL (post_type)
    и фактического типа объекта (object.type).
    """
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        url_post_type = self.kwargs.get('post_type')

        if not url_post_type or obj.type != url_post_type:
            raise Http404("Запрашиваемый ресурс не найден.")

        return obj
