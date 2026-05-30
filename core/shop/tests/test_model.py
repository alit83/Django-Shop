import pytest
from ..models import Product, ProductCategory, ProductStatus
from accounts.models import User, UserType


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
    main_cat = ProductCategory.objects.create(title="main")
    middle_cat = ProductCategory.objects.create(
        title="middle", parent=main_cat
    )
    return ProductCategory.objects.create(title="ps5", parent=middle_cat)


def test_create_product_with_valid_value(db, category, user):
    product = Product.objects.create(
        user=user,
        title="ps5 pro",
        price=3000000,
        stock=5,
        category=category,
        description="test test test test",
        brief_description="test",
        status=ProductStatus.publish.value,
    )
    assert product.title == "ps5 pro"
    assert product.price == 3000000
