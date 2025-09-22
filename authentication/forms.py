from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserForm(forms.ModelForm):
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Để trống nếu không đổi mật khẩu"
    )
    password_confirm = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(render_value=False),
        required=False
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 8})
    )

    class Meta:
        model = User
        fields = [
            "username", "email", "is_active", "is_staff", "is_superuser", "groups"
        ]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Tên đăng nhập"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        pwd2 = cleaned.get("password_confirm")
        if pwd or pwd2:
            if pwd != pwd2:
                self.add_error("password_confirm", "Mật khẩu xác nhận không khớp")
            if pwd and len(pwd) < 6:
                self.add_error("password", "Mật khẩu tối thiểu 6 ký tự")
        return cleaned


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.order_by("content_type__app_label", "codename"),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 14})
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Tên nhóm (ví dụ: editors)"}),
        }