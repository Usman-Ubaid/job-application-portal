from django.urls import path
from .views import JobDetailView, JobListCreateView
from applications.views import ApplyJobView, JobApplicantView

urlpatterns = [
    path("", JobListCreateView.as_view(), name="job-list-create"),
    path("<int:id>/", JobDetailView.as_view(), name="job-detail"),
    path("<int:id>/apply/", ApplyJobView.as_view(), name="job-apply"),
    path("<int:id>/applicants/", JobApplicantView.as_view(), name="job-applicants"),
]
