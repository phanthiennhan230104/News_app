from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(blank=True, null=True)  # thêm mô tả

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=500)
    content = models.TextField()
    published_at = models.DateTimeField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="articles")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["-published_at", "id"], name="idx_pub_id_desc"),
            models.Index(fields=["category", "-published_at", "id"], name="idx_cat_pub_desc"),
        ]
        ordering = ["-published_at", "-id"]

    def __str__(self):
        return self.title
