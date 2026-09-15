from rest_framework import serializers
from .models import JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "description",
            "location",
            "salary_range",
            "employment_type",
            "is_active",
            "created_at",
            "updated_at",
        ]
