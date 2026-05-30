from django.urls import path
from .. import views

urlpatterns = [
    path("user/list/", views.AdminUserListView.as_view(), name="user-list"),
    path(
        "user/<int:pk>/edit/",
        views.AdminUserEditView.as_view(),
        name="user-edit",
    ),
    path(
        "user/<int:pk>/delete/",
        views.AdminUserDeleteView.as_view(),
        name="user-delete",
    ),
]
