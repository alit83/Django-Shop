import pytest
from django.urls import reverse
from shop.models import Product, ProductCategory ,ProductStatus , WishlistProductModel
from pytest_django.asserts import assertTemplateUsed
from accounts.models import User , UserType
from cart.models import CartModel , CartItemModel
from order.models import UserAddressModel , OrderItemModel , OrderModel , OrderStatusType
from django.conf import settings
from unittest.mock import patch
import requests_mock

@pytest.fixture(autouse=True)
def disable_debug_toolbar(settings):
    settings.DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda request: False}

@pytest.fixture
def user(db):
    return User.objects.create(email='test_order@test.com',password='@A12345678',is_verified=True,type=UserType.customer.value)

@pytest.fixture
def category(db):
    main_cat = ProductCategory.objects.create(title="main" , slug='main')
    middle_cat = ProductCategory.objects.create(title="middle" , parent=main_cat , slug='middle')
    return ProductCategory.objects.create(title='ps5',parent=middle_cat ,slug='ps5')


@pytest.fixture
def product(db,category,user):
        return Product.objects.create(
        user= user,
        title="ps5 pro",
        price=3000000,
        slug="ps5-pro",
        stock=5,
        category = category,
        description = 'test test test test',
        brief_description = 'test',
        status = ProductStatus.publish.value,
    )

@pytest.fixture
def address(db ,  user):
    return UserAddressModel.objects.create(
         user = user,
        address = 'test plak 2',
        state = 'test',
        city = 'test city',
        zip_code = '2141341',

    )

@pytest.fixture
def cart(db ,  user):
    return CartModel.objects.create(
         user = user,

    )

@pytest.fixture
def cartitem(db , cart , product ):
    return CartItemModel.objects.create(
         cart=cart,
         product =product,
         quantity = 2.

    )


@pytest.fixture
def mock_zarinpal_success():
    with requests_mock.Mocker() as m:
        m.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
            json={"data": {"code": 100, "authority": "TEST_AUTHORITY"}}
        )
        yield m

@pytest.mark.django_db
def test__get__order_checkout_view_successful_response(client,user):
    client.force_login(user)
    url = reverse('order:checkout')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'order/checkout.html')


@pytest.mark.django_db
def test__post__order_checkout_view_successful_response( mock_zarinpal_success,client,user , address , product , cart , cartitem):
    client.force_login(user)
    url = reverse('order:checkout')
    data = {
         "address_id" : address.id
    }
    response = client.post(url , data)
    assert OrderModel.objects.filter(user=user).exists() == True
    order =OrderModel.objects.get(user=user)
    assert order.status == OrderStatusType.pending.value
    assert OrderItemModel.objects.filter(order=order).exists() == True