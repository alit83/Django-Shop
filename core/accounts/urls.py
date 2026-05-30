from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "registration/", views.RegistrationView.as_view(), name="registration"
    ),
    path(
        "check_verification/",
        views.CheckVerificationView.as_view(),
        name="check_verification",
    ),
    path(
        "wait_for_verification/",
        views.WaitForVerificationView.as_view(),
        name="wait_for_verification",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "verify-email/<token>/",
        views.VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "resend/verification-email/",
        views.ResendVerificationEmailView.as_view(),
        name="resend-verification-email",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "forget-password/",
        views.ForgetPasswordView.as_view(),
        name="forget-password",
    ),
]
