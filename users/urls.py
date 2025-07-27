from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import RegisterView, PleaseConfirmView, ActivateView

app_name = "users"

urlpatterns = [
    # Регистрация и активация
    path("register/", RegisterView.as_view(), name="register"),
    path("please-confirm/", PleaseConfirmView.as_view(), name="please_confirm"),
    path("activate/<str:token>/", ActivateView.as_view(), name="activate"),

    # Вход / Выход
    path("login/", auth_views.LoginView.as_view(
        template_name="users/login.html"
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Сброс пароля
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="users/password_reset.html",
        email_template_name="users/password_reset_email.html",
        success_url=reverse_lazy("users:password_reset_done")
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete")
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"
    ), name="password_reset_complete"),
]
