from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
class HasVerifiedPermission(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_verified
        return False
    def handle_no_permission(self):
        if not self.request.user.is_verified:
            return redirect(reverse_lazy('accounts:wait_for_verification'))
        return super().handle_no_permission()
