from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('news/', views.PostsList.as_view(), {'post_type': 'news'}, name='news'),
    path('news/<int:pk>', views.ShowPost.as_view(), {'post_type': 'news'}, name='new'),
    path('articles/', views.PostsList.as_view(), {'post_type': 'article'}, name='articles'),
    path('articles/<int:pk>', views.ShowPost.as_view(), {'post_type': 'article'}, name='article'),
    path('__debug__/', include("debug_toolbar.urls")),
]
