import pytest
from shop.models import Product, ProductCategory , ProductStatus
from accounts.models import User , UserType
from ..models import OrderModel , OrderStatusType ,OrderItemModel


@pytest.fixture
def user(db):
    return User.objects.create(email='test@test.com',password='@A12345678',is_verified=True,type=UserType.admin.value)



@pytest.fixture
def order(db ,  user):
    return OrderModel.objects.create(
         user = user,
        address = 'test plak 2',
        state = 'test',
        city = 'test city',
        zip_code = '2141341',
        total_price = 22222,
        status = OrderStatusType.pending.value

    )


@pytest.fixture
def category(db):
    main_cat = ProductCategory.objects.create(title="main")
    middle_cat = ProductCategory.objects.create(title="middle" , parent=main_cat)
    return ProductCategory.objects.create(title='ps5',parent=middle_cat)

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



def test_create_order_items_with_valid_value(db , order , product):
    order_item = OrderItemModel.objects.create(
        price=3000000,
        product =product,
        order=order,
        quantity = 4
    )
    assert order_item.order.zip_code == '2141341'
    assert order_item.price == 3000000
