#📰 News App – Hệ thống Tin tức Django

Ứng dụng web tin tức được xây dựng bằng Django + MySQL, hỗ trợ phân quyền người dùng: độc giả, người đăng tin, quản trị viên.

##🚀 Tính năng chính

✅ Đăng nhập / Đăng ký / Đăng xuất / Phân quyền

📰 Quản lý tin tức: đăng bài, chỉnh sửa, xoá bài (người đăng tin)

📚 Duyệt tin tức theo danh mục

🔍 Tìm kiếm bài viết

🛠️ Trang quản trị: quản lý người dùng, nhóm, phân quyền

🌍 Hỗ trợ dữ liệu lớn (MySQL, tối ưu bằng FULLTEXT Search)
## ⚙️ Yêu cầu hệ thống
<pre>
  pip install -r requirements.txt
</pre>
## 🛠️ Cài đặt và chạy hệ thống
<pre>
  git clone [https://github.com/phanthiennhan230104/ELearningProject.git](https://github.com/phanthiennhan230104/News_app.git)
  cd news-app
  pip install -r requirements.txt
</pre>

<pre>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_db',
        'USER': 'root', ## sửa theo máy
        'PASSWORD': '123456',  ## sửa theo máy
        'HOST': 'localhost',
        'PORT': '3306',
    }
}</pre>
## 🔐 Tài khoản mẫu
| Vai trò       | Tài khoản| Mật khẩu     |
| ------------- | ---------| ------------ |
| Quản trị viên | admin    | Nhan2004@    |
| Giảng viên    | report1  | Nhan2004@    |
| Sinh viên     | user     | Nhan2004@    |
## 📁 Cấu trúc thư mục
<pre>
  news-app/
│── manage.py
│── requirements.txt
│── README.md
│── .gitignore
│
├── venv/                      # Virtual environment (bỏ qua khi push git)
│
├── config/                    # Project config (settings, urls, wsgi, asgi)
│   │── __init__.py
│   │── asgi.py
│   │── settings.py
│   │── urls.py
│   │── wsgi.py
│   └── .env                   # File env (không push git)
│
├── authentication/            # App quản lý user, nhóm, login, register
│   │── __init__.py
│   │── admin.py
│   │── apps.py
│   │── forms.py
│   │── models.py
│   │── tests.py
│   │── urls.py
│   │── views.py
│   └── migrations/
│       └── __init__.py
│
├── core/                      # App chính (bài viết, danh mục)
│   │── __init__.py
│   │── admin.py
│   │── apps.py
│   │── models.py
│   │── tests.py
│   │── urls.py
│   │── views.py
│   └── migrations/
│       │── __init__.py
│       │── 0001_initial.py
│       └── 0002_category_description.py
│
├── templates/                 # Template HTML
│   │
│   ├── admin/                 # Template tuỳ chỉnh cho dashboard admin
│   │   └── base_site.html
│   │
│   ├── authentication/        # Template cho login, register, user CRUD
│   │   │── confirm_delete.html
│   │   │── group_form.html
│   │   │── login.html
│   │   │── register.html
│   │   └── user_form.html
│   │
│   └── core/                  # Template cho tin tức
│       │── base.html
│       │── home.html
│       │── article_form.html
│       │── article_detail.html
│       │── article_confirm_delete.html
│       │── by_category.html
│       │── my_articles.html
│       └── category_list.html
│
└── static/                    # Static files (CSS, JS, images)
    │
    ├── core/css/
    │   └── style.css
    │
    ├── admin/css/
    │   └── custom.css
    │
    └── authentication/css/
        │── login.css
        │── register.css
        └── superuser_home.css
</pre>

## RUN SERVER
<pre>
python manage.py runserver
Mở trình duyệt: http://127.0.0.1:8000</pre>

## 🤝 Đóng góp
Mọi đóng góp đều được chào đón. Vui lòng mở issue hoặc gửi pull request.
