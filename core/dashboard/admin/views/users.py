from django.views.generic import  ListView , UpdateView , DeleteView , CreateView
from accounts.models import  UserType , User
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from ..forms import AdminUserForm 
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
# Create your views here.

class AdminUserListView(HasAdminAccessPermission,LoginRequiredMixin,ListView):
    template_name = "dashboard/admin/users/user-list.html"
    paginate_by=9

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False,type=UserType.customer.value).order_by("-created_date")
        if search_q:=self.request.GET.get("q"):
            queryset=queryset.filter(email__icontains=search_q)
        if order:=self.request.GET.get("order_by"):
            try:
                queryset=queryset.order_by(order)
            except FieldError:
                pass
        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context

class AdminUserEditView(HasAdminAccessPermission,SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    template_name = "dashboard/admin/users/user-edit.html"
    form_class = AdminUserForm
    queryset = User.objects.filter(is_superuser=False,type=UserType.customer.value).order_by("-created_date")
    success_message = "ویرایش کاربر با موفقیت انجام شد"
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:user-edit" , kwargs={"pk":self.get_object().pk})
 
class AdminUserDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/users/user-delete.html"
    queryset =User.objects.filter(is_superuser=False,type=UserType.customer.value)
    success_url = reverse_lazy("dashboard:admin:user-list")
    success_message = "حذف کاربر با موفقیت انجام شد"