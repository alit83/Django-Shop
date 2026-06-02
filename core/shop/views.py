from django.views.generic import DetailView, ListView, View
from shop.models import (
    Product,
    ProductStatus,
    ProductCategory,
    WishlistProductModel,
    ProductAttribute,
    Attribute,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from review.models import ReviewModel, ReviewStatus
from django.http import JsonResponse
from django.db.models import Q, Subquery, OuterRef, Count
from django.shortcuts import get_object_or_404
from django.contrib.postgres.aggregates import ArrayAgg

# Create your views here.


class ShopProductsGridView(ListView):
    template_name = "shop/products-grid.html"
    paginate_by = 9

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        self._slug = slug
        self.cat = get_object_or_404(ProductCategory, slug=slug)
        queryset = Product.objects.filter(
            category__slug=self.cat.slug, status=ProductStatus.publish.value
        )
        query_params = self.request.GET
        if search_q := query_params.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if min_price := query_params.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := query_params.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order := query_params.get("order_by"):
            try:
                allowed_orders = [
                    "-created_date",
                    "price",
                    "created_date",
                    "-price",
                ]
                if order in allowed_orders:
                    queryset = queryset.order_by(order)
            except FieldError:
                pass
        attributes_filter = {}
        for key, value in query_params.items():
            if key.startswith("attribute-") and value:
                try:
                    attr_id = key.split("attribute-")[-1]
                    attributes_filter[attr_id] = value
                except ValueError:
                    pass
        if attributes_filter:
            combined_attribute_q = Q()
            for attr_id, attr_value in attributes_filter.items():
                subquery_attrs = ProductAttribute.objects.filter(
                    attribute__id=int(attr_id),
                    value=attr_value,
                    product_id=OuterRef("pk"),
                ).values("product_id")
                combined_attribute_q &= Q(id__in=Subquery(subquery_attrs))
            queryset = queryset.filter(combined_attribute_q)
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["title_slug"] = self._slug
        context["wishlist_items"] = (
            WishlistProductModel.objects.filter(
                user=self.request.user
            ).values_list("product__id", flat=True)
            if self.request.user.is_authenticated
            else []
        )
        attributes = Attribute.objects.filter(
            group__category=self.cat
        ).select_related("group__category")
        for attr in attributes:
            attr.distinct_values = attr.attribute_attributes.values_list(
                "value", flat=True
            ).distinct()
        context["attributes"] = attributes
        return context


class ShopProductsDetailView(DetailView):
    template_name = "shop/products-detail.html"
    queryset = Product.objects.filter(status=ProductStatus.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["is_wished"] = (
            WishlistProductModel.objects.filter(
                user=self.request.user, product__id=product.id
            ).exists()
            if self.request.user.is_authenticated
            else False
        )
        reviews = ReviewModel.objects.filter(
            product=product, status=ReviewStatus.accepted.value
        )
        context["reviews"] = reviews
        total_reviews = reviews.count()

        rate_counts = reviews.values("rate").annotate(
            count=Count("rate")
        )  # Count make group by rate
        counts_dict = {item["rate"]: item["count"] for item in rate_counts}
        for rate in range(1, 6):
            count = counts_dict.get(rate, 0)
            context[f"review_{rate}"] = count
            context[f"style_{rate}"] = (
                (100 * count / total_reviews) if total_reviews > 0 else 0
            )

        return context


class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ""
        if product_id:
            try:
                wishlist_item = WishlistProductModel.objects.get(
                    user=request.user, product__id=product_id
                )
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(
                    user=request.user, product_id=product_id
                )
                message = "محصول به لیست علایق اضافه شد"

        return JsonResponse({"message": message})


class ShopProductsCategoryView(ListView):
    template_name = "shop/products-categories.html"
    queryset = ProductCategory.objects.filter().exclude(parent=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parents_categories"] = ProductCategory.objects.filter(
            parent=None
        )
        categories = ProductCategory.objects.filter(
            category_child=None
        ).order_by("-created_date")[:2]
        for category in categories:
            category.new_products = category.category_product.filter(
                status=ProductStatus.publish.value
            )[:3]
            category.min_price = category.category_product.filter(
                status=ProductStatus.publish.value
            ).order_by("price")[:1]
        context["categories"] = categories
        return context


class ShopProductMainView(ListView):
    template_name = "shop/products-main.html"

    def get_queryset(self):
        self.slug = self.kwargs.get("slug")
        cat = get_object_or_404(ProductCategory, slug=self.slug, parent=None)
        queryset = Product.objects.filter(
            category__parent__parent__slug=cat.slug,
            status=ProductStatus.publish.value,
        ).select_related("category__parent__parent")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.slug
        categories = (
            ProductCategory.objects.filter(parent__parent__slug=self.slug)
            .select_related("parent__parent")
            .order_by("-created_date")[:3]
        )
        for category in categories:
            category.new_products = category.category_product.filter(
                status=ProductStatus.publish.value
            )[:3]
            category.min_price = category.category_product.filter(
                status=ProductStatus.publish.value
            ).order_by("price")[:1]
        context["categories"] = categories
        return context


class ShopProductMiddleView(ListView):
    template_name = "shop/products-middle.html"

    def get_queryset(self):
        self._slug = self.kwargs.get("slug")
        self.cat = get_object_or_404(ProductCategory, slug=self._slug)
        queryset = Product.objects.filter(
            category__parent__slug=self.cat.slug,
            status=ProductStatus.publish.value,
        ).select_related("category__parent")
        query_params = self.request.GET
        if search_q := query_params.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if min_price := query_params.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := query_params.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order := query_params.get("order_by"):
            try:
                allowed_orders = [
                    "-created_date",
                    "price",
                    "created_date",
                    "-price",
                ]
                if order in allowed_orders:
                    queryset = queryset.order_by(order)
            except FieldError:
                pass
        attributes_filter = {}
        for key, value in query_params.items():
            if key.startswith("attribute-") and value:
                try:
                    attr_id = key.split("attribute-")[-1]
                    attributes_filter[attr_id] = value
                except ValueError:
                    pass
        if attributes_filter:
            combined_attribute_q = Q()
            for attr_id, attr_value in attributes_filter.items():
                subquery_attrs = ProductAttribute.objects.filter(
                    value=attr_value, product_id=OuterRef("pk")
                ).values("product_id")
                combined_attribute_q &= Q(id__in=Subquery(subquery_attrs))
            queryset = queryset.filter(combined_attribute_q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["title_slug"] = self._slug
        context["wishlist_items"] = (
            WishlistProductModel.objects.filter(
                user=self.request.user
            ).values_list("product__id", flat=True)
            if self.request.user.is_authenticated
            else []
        )
        cat_child = ProductCategory.objects.filter(parent=self.cat)
        if not cat_child.exists():
            context["attributes"] = []
            return context

        attributes_per_cat = [
            set(
                Attribute.objects.filter(group__category=cat)
                .select_related("group__category")
                .values_list("title", flat=True)
            )
            for cat in cat_child
        ]
        common_titles = (
            set.intersection(*attributes_per_cat)
            if attributes_per_cat
            else set()
        )
        if not common_titles:
            context["attributes"] = []
            return context
        distinct_values_subquery = (
            ProductAttribute.objects.filter(
                attribute__title=OuterRef("title"),
                attribute__group__category__in=cat_child,
            )
            .select_related("attribute__group__category")
            .order_by()
            .values("attribute__title")
            .annotate(values=ArrayAgg("value", distinct=True))
            .values("values")[:1]
        )

        attributes = (
            Attribute.objects.filter(
                title__in=common_titles,
                group__category__in=cat_child,
            )
            .select_related("group", "group__category")
            .annotate(distinct_values=Subquery(distinct_values_subquery))
        ).distinct("title")
        context["attributes"] = attributes
        return context


class ShopProductsSearchView(ListView):
    template_name = "shop/products-search.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(status=ProductStatus.publish.value)
        query_params = self.request.GET
        if search_q := query_params.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if min_price := query_params.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := query_params.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order := query_params.get("order_by"):
            try:
                allowed_orders = [
                    "-created_date",
                    "price",
                    "created_date",
                    "-price",
                ]
                if order in allowed_orders:
                    queryset = queryset.order_by(order)
            except FieldError:
                pass
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["wishlist_items"] = (
            WishlistProductModel.objects.filter(
                user=self.request.user
            ).values_list("product__id", flat=True)
            if self.request.user.is_authenticated
            else []
        )
        return context
