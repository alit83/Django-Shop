from django.views.generic import (DetailView
,CreateView ,ListView)
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect , get_object_or_404
from django.core.exceptions import FieldError
from website.models import ContactModel
from django.db.models import Q




class AdminContactListView(LoginRequiredMixin, HasAdminAccessPermission,  ListView):
    template_name = "dashboard/admin/contacts/contact-list.html"

    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size',self.paginate_by)

    def get_queryset(self):
        queryset = ContactModel.objects.all().order_by("-created_date")
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter( Q(email__icontains=search_q))
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context
    
class AdminContactDetailView(LoginRequiredMixin, HasAdminAccessPermission,  DetailView):
    template_name = "dashboard/admin/contacts/contact-detail.html"
    def get_object(self , queryset=None):
        contact_obj = get_object_or_404(ContactModel,pk=self.kwargs.get("pk"))
        if not contact_obj.is_seen:
            contact_obj.is_seen = True
            contact_obj.save()
        return contact_obj
    