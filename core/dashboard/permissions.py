from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import UserType
from django.shortcuts import redirect
from django.urls import reverse_lazy


class HasCustomerAccessPermission(UserPassesTestMixin):
    def test_func(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.is_verified
        ):
            return self.request.user.type == UserType.customer.value
        return False

    def handle_no_permission(self):
        if not self.request.user.is_verified:
            return redirect(reverse_lazy("accounts:wait_for_verification"))
        return super().handle_no_permission()


class HasAdminAccessPermission(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.admin.value
        return False
