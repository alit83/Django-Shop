from django.shortcuts import render
from django.contrib.auth import views as auth_views, login, get_user_model
from accounts.forms import RegistrationForm, EmailForm, ResetPasswordForm
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import forms as auth_forms
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .permissions import OnlyUnAuthenticatedPermission
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .tasks import send_verify_email, send_reset_password_email
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
User = get_user_model()


class CustomTokenGenerator(PasswordResetTokenGenerator):
    pass


token_generator = CustomTokenGenerator()


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = auth_forms.AuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class RegistrationView(OnlyUnAuthenticatedPermission, FormView):
    template_name = "accounts/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:wait_for_verification")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        token = generate_email_verify_token(user)
        send_verify_email.delay(token, user.email)
        user.last_verification_email = timezone.now()
        user.save(update_fields=["last_verification_email"])
        return super().form_valid(form)


class ResendVerificationEmailView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_verified:
            messages.info(request, "ایمیل شما قبلا تاببد شده است.")
            return redirect("/")
        now = timezone.now()
        if (
            user.last_verification_email
            and now - user.last_verification_email < timedelta(minutes=2)
        ):
            remaining = 120 - int(
                (now - user.last_verification_email).total_seconds()
            )
            messages.error(request, f"لطفاً {remaining} ثانیه دیگر تلاش کنید.")
            return redirect(reverse_lazy("accounts:wait_for_verification"))
        token = generate_email_verify_token(user)
        send_verify_email.delay(token, user.email)
        user.last_verification_email = now
        user.save(update_fields=["last_verification_email"])
        messages.success(request, "لینک تایید ایمیل جدید برایتان ارسال شد")
        return redirect(reverse_lazy("accounts:wait_for_verification"))


def generate_email_verify_token(user):
    signer = TimestampSigner()
    raw_token = signer.sign(user.pk)
    return urlsafe_base64_encode(force_bytes(raw_token))


class WaitForVerificationView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/wait_for_verification.html"


class CheckVerificationView(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return JsonResponse({"verified": request.user.is_verified})


class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            signer = TimestampSigner()
            max_age_seconds = 60 * 60 * 12
            raw_token = force_str(urlsafe_base64_decode(token))
            user_pk = signer.unsign(raw_token, max_age=max_age_seconds)
            user = User.objects.get(pk=user_pk)
            if user.is_verified:
                return render(request, "accounts/already-verify-email.html")
            user.is_verified = True
            user.save()
            return render(request, "accounts/success-verify-email.html")
        except (BadSignature, SignatureExpired, User.DoesNotExist, ValueError):
            return render(request, "accounts/failed-verify-email.html")


class ForgetPasswordView(OnlyUnAuthenticatedPermission, FormView):
    template_name = "accounts/forget-password.html"
    form_class = EmailForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.success(
                self.request,
                "ایمیل تغییر رمز عبور با موفقیت برایتان ارسال شد.",
            )
        token = token_generator.make_token(user_obj)
        uidb64 = urlsafe_base64_encode(force_bytes(user_obj.pk))
        send_reset_password_email.delay(token, uidb64, user_obj.email)
        messages.success(
            self.request, "ایمیل تغییر رمز عبور با موفقیت برایتان ارسال شد."
        )
        return super().form_valid(form)


class ResetPasswordView(View):
    def get(self, request, token, uidb64, *args, **kwargs):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return render(request, "accounts/failed-reset-password.html")
        if not token_generator.check_token(user_obj, token):
            return render(request, "accounts/failed-reset-password.html")
        return render(request, "accounts/reset-password.html")

    def post(self, request, token, uidb64, *args, **kwargs):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return render(request, "accounts/failed-reset-password.html")
        if token_generator.check_token(user_obj, token):
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.clean_password()
                user_obj.set_password(password)
                user_obj.save()
                return render(request, "accounts/success-reset-password.html")

        return render(request, "accounts/failed-reset-password.html")
