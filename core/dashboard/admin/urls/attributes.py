from django.urls import path
from .. import views

urlpatterns = [
    path(
        "attribute/<int:pk>/create/",
        views.AdminAttributeCreateView.as_view(),
        name="attribute-create",
    ),
    path(
        "attribute/middle/<int:pk>/create/",
        views.AdminAttributeMiddleCreateView.as_view(),
        name="attribute-middle-create",
    ),
    path(
        "attribute/group/<int:pk>/create/",
        views.AdminAttributeGroupCreateView.as_view(),
        name="attribute-group-create",
    ),
    path(
        "attribute/<int:pk>/delete/",
        views.AdminAttributeDeleteView.as_view(),
        name="attribute-delete",
    ),
]
