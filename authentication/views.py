from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from .forms import UserForm, GroupForm
from core.models import Category

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser, login_url="login")
def superuser_home(request):
    users = User.objects.all().order_by("id")
    groups = Group.objects.all().order_by("id")
    categories = Category.objects.all().order_by("name")
    return render(request, "admin/base_site.html", {
        "users": users,
        "groups": groups,
        "categories": categories,
    })

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect("superuser_home")   # 👈 superuser → dashboard custom
            elif user.is_staff:
                return redirect("/admin/")          # staff → Django admin mặc định
            else:
                return redirect("home")             # user thường → trang home
        else:
            messages.error(request, "Sai tài khoản hoặc mật khẩu!")
    return render(request, "authentication/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Mời bạn đăng nhập.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"form": form})

@user_passes_test(is_superuser, login_url="login")
def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                is_active=form.cleaned_data["is_active"],
                is_staff=form.cleaned_data["is_staff"],
                is_superuser=form.cleaned_data["is_superuser"],
            )
            pwd = form.cleaned_data.get("password")
            if not pwd:
                messages.error(request, "Bạn phải nhập mật khẩu khi tạo tài khoản.")
            else:
                user.set_password(pwd)
                user.save()
                user.groups.set(form.cleaned_data["groups"])
                messages.success(request, f"Tạo tài khoản '{user.username}' thành công.")
                return redirect("superuser_home")
    else:
        form = UserForm(initial={"is_active": True})
    return render(request, "authentication/user_form.html", {"form": form, "mode": "create"})


@user_passes_test(is_superuser, login_url="login")
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            pwd = form.cleaned_data.get("password")
            if pwd:
                user.set_password(pwd)
            user.save()
            form.save_m2m()
            messages.success(request, f"Cập nhật tài khoản '{user.username}' thành công.")
            return redirect("superuser_home")
    else:
        form = UserForm(instance=user, initial={"groups": user.groups.all()})
    return render(request, "authentication/user_form.html", {"form": form, "mode": "update", "obj": user})


@user_passes_test(is_superuser, login_url="login")
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        uname = user.username
        user.delete()
        messages.success(request, f"Đã xoá tài khoản '{uname}'.")
        return redirect("superuser_home")
    return render(request, "authentication/confirm_delete.html", {
        "title": "Xoá tài khoản", "object_name": user.username, "cancel_url": reverse("superuser_home")
    })


# -----------------------
# Group CRUD
# -----------------------
@user_passes_test(is_superuser, login_url="login")
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo nhóm thành công.")
            return redirect("superuser_home")
    else:
        form = GroupForm()
    return render(request, "authentication/group_form.html", {"form": form, "mode": "create"})


@user_passes_test(is_superuser, login_url="login")
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật nhóm thành công.")
            return redirect("superuser_home")
    else:
        form = GroupForm(instance=group)
    return render(request, "authentication/group_form.html", {"form": form, "mode": "update", "obj": group})


@user_passes_test(is_superuser, login_url="login")
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        name = group.name
        group.delete()
        messages.success(request, f"Đã xoá nhóm '{name}'.")
        return redirect("superuser_home")
    return render(request, "authentication/confirm_delete.html", {
        "title": "Xoá nhóm", "object_name": group.name, "cancel_url": reverse("superuser_home")
    })

from core.models import Category

@user_passes_test(is_superuser, login_url="login")
def category_create(request):
    if request.method == "POST":
        name = (request.POST.get("title") or "").strip()
        slug = (request.POST.get("short_desc") or "").strip()
        description = (request.POST.get("content") or "").strip()

        if not (name and slug):
            messages.error(request, "Tên và slug là bắt buộc.")
        else:
            Category.objects.create(name=name, slug=slug, description=description)
            messages.success(request, "Tạo chuyên mục thành công.")
            return redirect("superuser_home")

    return render(request, "core/article_form.html", {"category_mode": True})


@user_passes_test(is_superuser, login_url="login")
def category_update(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        cat.name = request.POST.get("title") or cat.name
        cat.slug = request.POST.get("short_desc") or cat.slug
        cat.description = request.POST.get("content") or cat.description
        cat.save()
        messages.success(request, "Cập nhật chuyên mục thành công.")
        return redirect("superuser_home")

    return render(request, "core/article_form.html", {"category_mode": True, "cat": cat})


@user_passes_test(is_superuser, login_url="login")
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        cname = cat.name
        cat.delete()
        messages.success(request, f"Đã xoá chuyên mục '{cname}'.")
        return redirect("superuser_home")

    return render(request, "core/confirm_delete.html", {
        "title": "Xoá chuyên mục",
        "object_name": cat.name,
        "cancel_url": reverse("superuser_home"),
    })

@user_passes_test(is_superuser)
def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "core/category_list.html", {"categories": categories})