from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/applications/", include("applications.urls")),
    path("api/companies/", include("companies.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
