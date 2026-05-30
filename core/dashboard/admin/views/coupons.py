from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from order.models import CouponModel
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from ..forms import CouponForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.


class AdminCouponListView(
    HasAdminAccessPermission, LoginRequiredMixin, ListView
):
    template_name = "dashboard/admin/coupon/coupon-list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = CouponModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(code__icontains=search_q)
        if order := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order)
            except FieldError:
                pass
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context


class AdminCouponEditView(
    HasAdminAccessPermission,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UpdateView,
):
    template_name = "dashboard/admin/coupon/coupon-edit.html"
    form_class = CouponForm
    queryset = CouponModel.objects.all()
    success_message = "ویرایش تخفیف با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:coupons-edit", kwargs={"pk": self.get_object().pk}
        )


class AdminCouponDeleteView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "dashboard/admin/coupon/coupon-delete.html"
    queryset = CouponModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:coupons-list")
    success_message = "حذف تخفیف با موفقیت انجام شد"


class AdminCouponCreateView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "dashboard/admin/coupon/coupon-create.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_message = "ایجاد تخفیف با موفقیت انجام شد"

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(
            reverse_lazy(
                "dashboard:admin:coupons-edit", kwargs={"pk": form.instance.pk}
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupons-list")
