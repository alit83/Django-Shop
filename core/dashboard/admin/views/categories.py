from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from shop.models import ProductCategory
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from ..forms import AdminCategoryForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.


class AdminCategoryCreateView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "dashboard/admin/categories/category-create.html"
    queryset = ProductCategory.objects.all()
    form_class = AdminCategoryForm
    success_message = "ایجاد دسته بندی با موفقیت انجام شد"

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(
            reverse_lazy(
                "dashboard:admin:category-edit",
                kwargs={"pk": form.instance.pk},
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:category-list")


class AdminCategoryListView(
    HasAdminAccessPermission, LoginRequiredMixin, ListView
):
    template_name = "dashboard/admin/categories/category-list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = ProductCategory.objects.all().order_by("parent")
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
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


class AdminCategoryEditView(
    HasAdminAccessPermission,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UpdateView,
):
    template_name = "dashboard/admin/categories/category-edit.html"
    form_class = AdminCategoryForm
    queryset = ProductCategory.objects.all()
    success_message = "ویرایش  دسته بندی  با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:category-edit",
            kwargs={"pk": self.get_object().pk},
        )


class AdminCategoryDeleteView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "dashboard/admin/categories/category-delete.html"
    queryset = ProductCategory.objects.all()
    success_url = reverse_lazy("dashboard:admin:category-list")
    success_message = "حذف دسته بندی با موفقیت انجام شد"
