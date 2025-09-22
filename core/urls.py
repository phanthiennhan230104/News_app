from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.by_category, name="by_category"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),

    path("me/articles/", views.my_articles, name="my_articles"),
    path("me/articles/new/", views.article_create, name="article_create"),
    path("me/articles/<int:pk>/edit/", views.article_update, name="article_update"),
    path("me/articles/<int:pk>/delete/", views.article_delete, name="article_delete"),

]
