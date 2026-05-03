from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('news/', views.PostsList.as_view(), {'post_type': 'news'}, name='news'),
    path('news/<int:pk>', views.ShowPost.as_view(), {'post_type': 'news'}, name='new'),
    path('news/create/', views.AddPost.as_view(), {'post_type': 'news'}, name='addnews'),
    path('news/<int:pk>/edit/', views.UpdatePost.as_view(), {'post_type': 'news'}, name='updatenews'),
    path('news/<int:pk>/delete/', views.DeletePost.as_view(), {'post_type': 'news'}, name='deletenews'),
    path('articles/', views.PostsList.as_view(), {'post_type': 'article'}, name='articles'),
    path('articles/<int:pk>', views.ShowPost.as_view(), {'post_type': 'article'}, name='article'),
    path('articles/create/', views.AddPost.as_view(), {'post_type': 'article'}, name='addarticles'),
    path('articles/<int:pk>/edit/', views.UpdatePost.as_view(), {'post_type': 'article'}, name='updatearticles'),
    path('articles/<int:pk>/delete/', views.DeletePost.as_view(), {'post_type': 'article'}, name='deletearticles'),
    path('news/search/', views.PostsList.as_view(), {'post_type': 'news'}, name='newsearch'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('subscribe_ot/<int:pk>', views.subscribe_ot, name='subscribe_ot'),
    path('__debug__/', include("debug_toolbar.urls")),

]


# /news/create/
# /news/<int:pk>/edit/
# /news/<int:pk>/delete/
# /articles/create/
# /articles/<int:pk>/edit/
# /articles/<int:pk>/delete/