from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(read_only=True)
    applicant = serializers.StringRelatedField(read_only=True)
    status = serializers.ReadOnlyField()
    applied_at = serializers.ReadOnlyField()

    class Meta:
        model = Application
        fields = ["id", "job", "applicant", "cover_letter", "status", "applied_at"]


class ApplicationStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Application.STATUS)

    class Meta:
        model = Application
        fields = ["id", "status"]
