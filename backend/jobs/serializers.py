from rest_framework import serializers
from .models import JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    company_name = serializers.CharField(
        source="employer.companyprofile.company_name",
        read_only=True,
        allow_null=True,
        default=None,
    )
    company_address = serializers.CharField(
        source="employer.companyprofile.address",
        read_only=True,
        allow_null=True,
        default=None,
    )

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "description",
            "location",
            "salary_range",
            "employment_type",
            "company_name",
            "company_address",
            "is_active",
            "created_at",
            "updated_at",
        ]
