from django.contrib import admin
from .models import Category, Article
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","slug")
    search_fields = ("name","slug")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id","title","category","author","published_at","updated_at")
    list_filter = ("category",)
    search_fields = ("title","short_desc")
    autocomplete_fields = ("category","author")
