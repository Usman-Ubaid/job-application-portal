from django.urls import path
from .views import (
    SeekerApplicationsView,
    UpdateApplicationStatusView,
)

urlpatterns = [
    path(
        "mine/",
        SeekerApplicationsView.as_view(),
        name="my-application",
    ),
    path(
        "<int:id>/",
        UpdateApplicationStatusView.as_view(),
        name="application-status-update",
    ),
]
