from django.contrib import admin
from django.urls import path, include
from rooms import views  # <-- ADD THIS IMPORT

urlpatterns = [
    path("admin/", admin.site.urls),

    # App URLs
    path("", include("rooms.urls")),

    # Auth system but using CUSTOM login
    path("accounts/login/", views.custom_login, name="login"),

    # Logout
    path("accounts/logout/",
         views.logout_view,
         name="logout"),

    # Built-in password reset etc.
    path("accounts/", include("django.contrib.auth.urls")),
]
