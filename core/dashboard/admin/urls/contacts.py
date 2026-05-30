from django.urls import path
from .. import views

urlpatterns = [
    path(
        "contact/list/",
        views.AdminContactListView.as_view(),
        name="contact-list",
    ),
    path(
        "contact/<int:pk>/detail/",
        views.AdminContactDetailView.as_view(),
        name="contact-detail",
    ),
]
