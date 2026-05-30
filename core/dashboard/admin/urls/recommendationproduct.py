from django.urls import path
from .. import views

urlpatterns = [
    path(
        "recommendation/list/",
        views.AdminRecommendationListView.as_view(),
        name="recommendation-list",
    ),
    path(
        "recommendation/create/",
        views.AdminRecommendationCreateView.as_view(),
        name="recommendation-create",
    ),
    path(
        "recommendation/<int:pk>/delete/",
        views.AdminRecommendationDeleteView.as_view(),
        name="recommendation-delete",
    ),
]
