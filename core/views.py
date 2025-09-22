from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from .models import Article, Category

PAGE_SIZE = 20


def home(request):
    q = (request.GET.get("q") or "").strip()
    page = int(request.GET.get("page", "1"))
    offset = (page - 1) * PAGE_SIZE

    if q:
        articles = Article.objects.filter(
            Q(title__icontains=q) | Q(short_desc__icontains=q) | Q(content__icontains=q)
        ).order_by("-published_at", "-id")[offset:offset + PAGE_SIZE]
    else:
        articles = Article.objects.all().order_by("-published_at", "-id")[offset:offset + PAGE_SIZE]

    ctx = {
        "articles": articles,
        "q": q,
        "page": page,
        "can_post": _can_post(request.user) if request.user.is_authenticated else False,
    }
    return render(request, "core/home.html", ctx)


def by_category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    page = int(request.GET.get("page", "1"))
    offset = (page - 1) * PAGE_SIZE
    articles = Article.objects.filter(category=cat).order_by("-published_at", "-id")[offset:offset + PAGE_SIZE]
    return render(request, "core/by_category.html", {"category": cat, "articles": articles, "page": page})


def article_detail(request, pk):
    a = get_object_or_404(Article, pk=pk)
    return render(request, "core/article_detail.html", {"a": a})


# ====== CRUD cho nhóm Người đăng tin hoặc superuser ======

def _can_post(user):
    return user.is_superuser or user.groups.filter(name="Người đăng tin").exists()


@login_required
def my_articles(request):
    if not _can_post(request.user):
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect("home")

    articles = Article.objects.filter(author=request.user).order_by("-published_at", "-id")[:200]
    return render(request, "core/my_articles.html", {"articles": articles})


@login_required
def article_create(request):
    if not _can_post(request.user):
        messages.error(request, "Bạn không có quyền đăng bài.")
        return redirect("home")

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        short_desc = (request.POST.get("short_desc") or "").strip()
        content = (request.POST.get("content") or "").strip()
        category_id = request.POST.get("category_id")
        published_at = request.POST.get("published_at") or timezone.now()

        if not (title and short_desc and content and category_id):
            messages.error(request, "Thiếu dữ liệu bắt buộc.")
        else:
            Article.objects.create(
                title=title,
                short_desc=short_desc,
                content=content,
                category_id=category_id,
                author=request.user,
                published_at=published_at,
            )
            messages.success(request, "Đăng tin thành công.")
            return redirect("my_articles")

    categories = Category.objects.all().order_by("name")
    return render(request, "core/article_form.html", {"categories": categories})


@login_required
def article_update(request, pk):
    if not _can_post(request.user):
        messages.error(request, "Bạn không có quyền sửa bài.")
        return redirect("home")

    a = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        a.title = request.POST.get("title") or a.title
        a.short_desc = request.POST.get("short_desc") or a.short_desc
        a.content = request.POST.get("content") or a.content
        a.category_id = request.POST.get("category_id") or a.category_id
        a.published_at = request.POST.get("published_at") or a.published_at
        a.save()
        messages.success(request, "Cập nhật thành công.")
        return redirect("my_articles")

    categories = Category.objects.all().order_by("name")
    return render(request, "core/article_form.html", {"a": a, "categories": categories})


@login_required
def article_delete(request, pk):
    if not _can_post(request.user):
        messages.error(request, "Bạn không có quyền xoá bài.")
        return redirect("home")

    a = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        a.delete()
        messages.success(request, "Đã xoá.")
        return redirect("my_articles")
    return render(request, "core/article_confirm_delete.html", {"a": a})




