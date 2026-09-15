from django.urls import path
from .views import JobDetailView, JobListCreateView

urlpatterns = [
    path("", JobListCreateView.as_view(), name="job-list-create"),
    path("<int:id>/", JobDetailView.as_view(), name="job-detail"),
]
