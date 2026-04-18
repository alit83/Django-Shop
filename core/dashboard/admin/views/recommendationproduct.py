from django.views.generic import  ListView , UpdateView , DeleteView , CreateView
from shop.models import Product , ProductCategory , ProductImage , RecommendationProductModel
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from ..forms import AdminRecommendationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.urls import reverse_lazy
# Create your views here.

# Create your views here.

class AdminRecommendationListView(HasAdminAccessPermission,LoginRequiredMixin,ListView):
    template_name = "dashboard/admin/recommendation/recommendation-list.html"
    queryset = RecommendationProductModel.objects.all()
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["total_items"]=self.get_queryset().count()
        context["categories"]= ProductCategory.objects.filter().exclude(parent__parent=None)
        context["recommendation_form"]=AdminRecommendationForm
        return context

class AdminRecommendationDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    queryset = RecommendationProductModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:recommendation-list")
    success_message = " این محصول از بخش پیشنهادات حذف شد"

class AdminRecommendationCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    queryset = RecommendationProductModel.objects.all()
    form_class = AdminRecommendationForm
    success_url = reverse_lazy("dashboard:admin:recommendation-list")
    success_message = " این محصول به بخش پیشنهادات اضافه شد"
