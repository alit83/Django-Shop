from django.urls import path 
from .. import views
urlpatterns = [
    path("product/list/",views.AdminProductListView.as_view(),name="products-list"),
    path("product/create/",views.AdminProductCreateView.as_view(),name="products-create"),
    path("product/create/<int:pk>/image",views.AdminProductCreateImageView.as_view(),name="products-create-image"),
    path("product/delete/<int:product_pk>/image/<int:pk>/",views.AdminProductDeleteImageView.as_view(),name="products-delete-image"),
    path("product/<int:pk>/edit/",views.AdminProductEditView.as_view(),name="products-edit"),
    path("product/<int:pk>/delete/",views.AdminProductDeleteView.as_view(),name="products-delete"),
]
