from django.urls import path
from .views import (
    CompanyProfileView,
    CompanyDetailView,
)

urlpatterns = [
    path(
        "mine/",
        CompanyProfileView.as_view(),
        name="my-company",
    ),
    path(
        "<int:id>/",
        CompanyDetailView.as_view(),
        name="company-detail",
    ),
]
