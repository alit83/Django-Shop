from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from shop.models import (
    Product,
    ProductCategory,
    ProductImage,
    AttributeGroup,
    Attribute,
    ProductAttribute,
)
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from ..forms import AdminProductForm, AdminCreateImageForm, AdminCategoryForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.urls import reverse_lazy

# Create your views here.


class AdminProductListView(
    HasAdminAccessPermission, LoginRequiredMixin, ListView
):
    template_name = "dashboard/admin/product/product-list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
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
        context["categories"] = ProductCategory.objects.filter().exclude(
            parent__parent=None
        )
        return context


class AdminProductEditView(
    HasAdminAccessPermission,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UpdateView,
):
    template_name = "dashboard/admin/product/product-edit.html"
    form_class = AdminProductForm
    queryset = Product.objects.all()
    success_message = "ویرایش محصول با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:products-edit",
            kwargs={"pk": self.get_object().pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = AdminCreateImageForm()
        product = self.get_object()
        attribute_group = AttributeGroup.objects.filter(
            attributes_group__attribute_attributes__product=product,
            category=product.category,
        ).distinct()
        attributes_q = attribute_group.prefetch_related(
            Prefetch(
                "attributes_group",
                queryset=Attribute.objects.filter(
                    attribute_attributes__product=product
                ),
                to_attr="product_attributes",
            )
        )
        context["attributes_group"] = attributes_q.prefetch_related(
            Prefetch(
                "product_attributes__attribute_attributes",
                queryset=ProductAttribute.objects.filter(product=product),
                to_attr="product_values",
            )
        )

        return context


class AdminProductDeleteView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "dashboard/admin/product/product-delete.html"
    queryset = Product.objects.all()
    success_url = reverse_lazy("dashboard:admin:products-list")
    success_message = "حذف محصول با موفقیت انجام شد"


class AdminProductDeleteImageView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    DeleteView,
):
    http_method_names = ["post"]
    queryset = ProductImage.objects.all()
    success_message = "حذف تصویر با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:products-edit",
            kwargs={"pk": self.kwargs.get("product_pk")},
        )


class AdminProductCreateView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "dashboard/admin/product/product-create.html"
    queryset = Product.objects.all()
    form_class = AdminProductForm
    success_message = "ایجاد محصول با موفقیت انجام شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(
            reverse_lazy(
                "dashboard:admin:products-edit",
                kwargs={"pk": form.instance.pk},
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:products-list")


class AdminCategoryCreateView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "dashboard/admin/product/category-create.html"
    queryset = ProductCategory.objects.all()
    form_class = AdminCategoryForm
    success_message = "ایجاد دسته بندی با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:category-create")


class AdminProductCreateImageView(
    LoginRequiredMixin,
    HasAdminAccessPermission,
    SuccessMessageMixin,
    CreateView,
):
    http_method_names = ["post"]
    queryset = ProductImage.objects.all()
    form_class = AdminCreateImageForm
    success_message = "ایجاد تصویر محصول با موفقیت انجام شد"

    def form_valid(self, form):

        super().form_valid(form)
        product_obj = Product.objects.get(pk=self.kwargs.get("pk"))
        product_obj.image.add(form.instance)
        return redirect(
            reverse_lazy(
                "dashboard:admin:products-edit",
                kwargs={"pk": self.kwargs.get("pk")},
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:products-list")
