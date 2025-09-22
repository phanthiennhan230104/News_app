from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("superuser/", views.superuser_home, name="superuser_home"),

    # Users
    path("users/new/", views.user_create, name="user_create"),
    path("users/<int:pk>/edit/", views.user_update, name="user_update"),
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),

    # Groups
    path("groups/new/", views.group_create, name="group_create"),
    path("groups/<int:pk>/edit/", views.group_update, name="group_update"),
    path("groups/<int:pk>/delete/", views.group_delete, name="group_delete"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/new/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
]
