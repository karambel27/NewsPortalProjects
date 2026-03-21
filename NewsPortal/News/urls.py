from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('news/', views.NewsList.as_view(), name='newss'),
    path('news/<int:pk>', views.PostList.as_view(), name='news'),
    path('article/', views.ArticleList.as_view(), name='articlee'),
    path('article/<int:pk>', views.PostList.as_view(), name='article')
]
