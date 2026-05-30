from django.views.generic import ListView, DeleteView
from website.models import NewsLetterModel
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

# Create your views here.


class AdminNewsLetterListView(
    HasAdminAccessPermission, LoginRequiredMixin, ListView
):
    template_name = "dashboard/admin/newsletters/newsletter-list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = NewsLetterModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(email__icontains=search_q)
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


class AdminNewsLetterDeleteView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "dashboard/admin/newsletters/newsletter-delete.html"
    queryset = NewsLetterModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:newsletter-list")
    success_message = "عضو مورد نظر با موفقیت حذف شد"
