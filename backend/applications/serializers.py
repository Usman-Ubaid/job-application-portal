from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    cv = serializers.FileField()
    cover_letter_type = serializers.ReadOnlyField()
    job = serializers.PrimaryKeyRelatedField(read_only=True)
    applicant = serializers.StringRelatedField(read_only=True)
    status = serializers.ReadOnlyField()
    applied_at = serializers.ReadOnlyField()

    def validate(self, attrs):
        text = attrs.get("cover_letter_text")
        file = attrs.get("cover_letter_file")

        if text and file:
            raise serializers.ValidationError(
                "Only one type of cover letter can be submitted."
            )

        if text:
            attrs["cover_letter_type"] = Application.COVER_LETTER_TEXT
        elif file:
            attrs["cover_letter_type"] = Application.COVER_LETTER_FILE
        else:
            attrs["cover_letter_type"] = None

        return attrs

    class Meta:
        model = Application
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "cv",
            "job",
            "applicant",
            "cover_letter_text",
            "cover_letter_file",
            "cover_letter_type",
            "status",
            "applied_at",
        ]


class ApplicationStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Application.STATUS)

    class Meta:
        model = Application
        fields = ["id", "status"]
