from django.urls import path 
from .. import views
urlpatterns = [
    path("coupon/list/",views.AdminCouponListView.as_view(),name="coupons-list"),
    path("coupon/create/",views.AdminCouponCreateView.as_view(),name="coupons-create"),
    path("coupon/<int:pk>/edit/",views.AdminCouponEditView.as_view(),name="coupons-edit"),
    path("coupon/<int:pk>/delete/",views.AdminCouponDeleteView.as_view(),name="coupons-delete"),
]
