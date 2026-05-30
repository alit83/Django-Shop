from django.urls import path, re_path
from shop import views

app_name = "shop"
urlpatterns = [
    re_path(
        r"products/(?P<slug>[-\w]+)/grid/",
        views.ShopProductsGridView.as_view(),
        name="products-grid",
    ),
    path(
        "category/", views.ShopProductsCategoryView.as_view(), name="category"
    ),
    path(
        "search/",
        views.ShopProductsSearchView.as_view(),
        name="product-search",
    ),
    re_path(
        r"main/(?P<slug>[-\w]+)/",
        views.ShopProductMainView.as_view(),
        name="main",
    ),
    re_path(
        r"middle/(?P<slug>[-\w]+)/",
        views.ShopProductMiddleView.as_view(),
        name="middle",
    ),
    re_path(
        r"products/(?P<slug>[-\w]+)/detail/",
        views.ShopProductsDetailView.as_view(),
        name="products-detail",
    ),
    path(
        "add-or-remove-wishlist/",
        views.AddOrRemoveWishlistView.as_view(),
        name="add-or-remove-wishlist",
    ),
]
