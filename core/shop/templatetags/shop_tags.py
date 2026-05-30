from django import template
from shop.models import (
    ProductStatus,
    Product,
    WishlistProductModel,
)
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag("includes/latest-products.html", takes_context=True)
def show_latest_products(context):
    request = context.get("request")
    latest_products = cache.get("latest_products_tag")
    if latest_products is None:
        latest_products = (
            Product.objects.filter(status=ProductStatus.publish.value)
            .distinct()
            .order_by("-created_date")[:8]
        )
        cache.set("latest_products_tag", latest_products, 1800)
    wishlist_items = (
        WishlistProductModel.objects.filter(user=request.user).values_list(
            "product__id", flat=True
        )
        if request.user.is_authenticated
        else []
    )
    result = {
        "latest_products": latest_products,
        "user": request.user,
        "wishlist_items": wishlist_items,
    }

    return result


@register.inclusion_tag("includes/similar-products.html", takes_context=True)
def show_similar_products(context, prod):
    request = context.get("request")
    product_categories = prod.category
    similar_prodcuts = (
        Product.objects.filter(
            status=ProductStatus.publish.value, category=product_categories
        )
        .distinct()
        .exclude(id=prod.id)
        .order_by("-created_date")[:4]
    )
    wishlist_items = (
        WishlistProductModel.objects.filter(user=request.user).values_list(
            "product__id", flat=True
        )
        if request.user.is_authenticated
        else []
    )
    return {
        "similar_prodcuts": similar_prodcuts,
        "request": request,
        "wishlist_items": wishlist_items,
    }


@register.inclusion_tag(
    "includes/latest-three-products.html", takes_context=True
)
def show_three_products(context):
    request = context.get("request")
    latest_products = (
        Product.objects.filter(status=ProductStatus.publish.value)
        .distinct()
        .order_by("-created_date")[:4]
    )
    wishlist_items = (
        WishlistProductModel.objects.filter(user=request.user).values_list(
            "product__id", flat=True
        )
        if request.user.is_authenticated
        else []
    )
    return {
        "latest_products": latest_products,
        "request": request,
        "wishlist_items": wishlist_items,
    }


@register.inclusion_tag("includes/latest-products.html", takes_context=True)
def show_latest_products_main(context, category_slug):
    request = context.get("request")
    latest_products = (
        Product.objects.filter(
            status=ProductStatus.publish.value,
            category__parent__parent__slug=category_slug,
        )
        .select_related("category__parent__parent")
        .distinct()
        .order_by("-created_date")[:4]
    )
    wishlist_items = (
        WishlistProductModel.objects.filter(user=request.user).values_list(
            "product__id", flat=True
        )
        if request.user.is_authenticated
        else []
    )
    return {
        "latest_products": latest_products,
        "request": request,
        "wishlist_items": wishlist_items,
    }
