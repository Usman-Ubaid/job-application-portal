from rest_framework import serializers
from .models import CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "company_name",
            "address",
            "description",
            "website",
            "user",
            "created_at",
        ]
