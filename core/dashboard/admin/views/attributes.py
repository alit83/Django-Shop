from django.views.generic import  ListView , UpdateView , DeleteView , CreateView
from shop.models import ProductAttribute , Product  , Attribute , AttributeGroup
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from ..forms import AdminProductAttributeForm , AdminAttributeMiddleForm , AdminAttributeGroupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, transaction
from django.shortcuts import redirect , get_object_or_404
from django.urls import reverse_lazy
# Create your views here.



class AdminAttributeCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/attributes/attribute-create.html"
    form_class = AdminProductAttributeForm
    queryset = ProductAttribute.objects.all()
    success_message = "اضافه شدن ویژگی با موفقیت انجام شد"
    def form_valid(self, form):
        product = get_object_or_404(Product,pk=self.kwargs.get("pk"))
        form.instance.product = product
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            raise IntegrityError(".این ویژگی قبلا اضافه شده است")
        return super().form_valid(form)
    
    def get_success_url(self):
         
        return reverse_lazy("dashboard:admin:products-edit", kwargs={"pk":self.kwargs.get("pk")})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk= self.kwargs.get("pk")
        context['productPK']=pk
        category = get_object_or_404(Product,pk=pk).category
        context['attributes'] =Attribute.objects.filter(group__category=category).select_related('group__category')
        context['attributegroup'] =AttributeGroup.objects.filter(category=category)
        context['attribute_middle_form'] = AdminAttributeMiddleForm()
        context['attribute_group_form'] = AdminAttributeGroupForm()
        return context

class AdminAttributeDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/attributes/attribute-delete.html"
    queryset = ProductAttribute.objects.all()
    success_url = reverse_lazy("dashboard:admin:attribute-list")
    success_message = "حذف ویژگی با موفقیت انجام شد"
class AdminAttributeMiddleCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    http_method_names = ["post"]
    queryset = Attribute.objects.all()
    form_class = AdminAttributeMiddleForm
    success_message = "ایجاد ویژگی با موفقیت انجام شد"

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
class AdminAttributeGroupCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    http_method_names = ["post"]
    queryset = AttributeGroup.objects.all()
    form_class = AdminAttributeGroupForm
    success_message = "ایجاد دسته ویژگی با موفقیت انجام شد"
    def form_valid(self, form):
        product = get_object_or_404(Product,pk=self.kwargs.get("pk"))
        form.instance.category = product.category
        return super().form_valid(form)
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')