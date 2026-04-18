from django.urls import path
from . import views
app_name = "cart"
urlpatterns = [
    path("session/add-products/",views.SessionAddProductsView.as_view(),name="session-add-products"),
     path("session/reduce-products/",views.SessionReduceProductsView.as_view(),name="session-reduce-products"),
    path("session/remove-products/",views.SessionRemoveProductsView.as_view(),name="session-remove-products"),
    path("session/update-products-quantity/",views.SessionUpdateProductsQuantityView.as_view(),name="session-update-products-quantity"),
    path("session/cart/summary",views.SessionCartSummaryView.as_view(),name="session-cart-summary"),
]
