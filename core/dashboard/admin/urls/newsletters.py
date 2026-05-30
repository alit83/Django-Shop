from django.urls import path
from .. import views

urlpatterns = [
    path(
        "newsletter/list/",
        views.AdminNewsLetterListView.as_view(),
        name="newsletter-list",
    ),
    path(
        "newsletter/<int:pk>/delete/",
        views.AdminNewsLetterDeleteView.as_view(),
        name="newsletter-delete",
    ),
]
