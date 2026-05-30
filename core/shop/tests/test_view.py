import pytest
from django.urls import reverse
from ..models import (
    Product,
    ProductCategory,
    ProductStatus,
    WishlistProductModel,
)
from pytest_django.asserts import assertTemplateUsed
from accounts.models import User, UserType


@pytest.fixture(autouse=True)
def disable_debug_toolbar(settings):
    settings.DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: False
    }


@pytest.fixture
def user(db):
    return User.objects.create(
        email="test@test.com",
        password="@A12345678",
        is_verified=True,
        type=UserType.admin.value,
    )


@pytest.fixture
def category(db):
    main_cat = ProductCategory.objects.create(title="main", slug="main")
    middle_cat = ProductCategory.objects.create(
        title="middle", parent=main_cat, slug="middle"
    )
    return ProductCategory.objects.create(
        title="ps5", parent=middle_cat, slug="ps5"
    )


@pytest.fixture
def product(db, category, user):
    return Product.objects.create(
        user=user,
        title="ps5 pro",
        price=3000000,
        slug="ps5-pro",
        stock=5,
        category=category,
        description="test test test test",
        brief_description="test",
        status=ProductStatus.publish.value,
    )


@pytest.mark.django_db
def test_product_main_view_successful_response(client, category):
    url = reverse("shop:main", kwargs={"slug": category.parent.parent.slug})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/products-main.html")


@pytest.mark.django_db
def test_product_middle_view_successful_response(client, category, product):
    url = reverse("shop:middle", kwargs={"slug": category.parent.slug})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/products-middle.html")

    assert response.context["total_items"] == 1


@pytest.mark.django_db
def test_product_grid_view_successful_response(client, category, product):
    url = reverse("shop:products-grid", kwargs={"slug": category.slug})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/products-grid.html")
    assert response.context["total_items"] == 1


@pytest.mark.django_db
def test_product_detail_view_successful_response(client, product):
    url = reverse("shop:products-detail", kwargs={"slug": product.slug})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/products-detail.html")


@pytest.mark.django_db
def test_AddOrRemoveWishlist_view_successful_response(client, product, user):
    client.force_login(user)
    url = reverse("shop:add-or-remove-wishlist")
    response = client.post(url, {"product_id": product.id})
    assert response.status_code == 200
    assert (
        WishlistProductModel.objects.filter(product_id=product.id).exists()
    )
