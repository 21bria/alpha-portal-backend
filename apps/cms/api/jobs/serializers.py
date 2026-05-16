from rest_framework import serializers
from apps.cms.models import JobVacancy


class JobVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobVacancy
        fields = [
            "id",
            "title",
            "slug",
            "department",
            "location",
            "employment_type",
            "summary",
            "responsibilities",
            "requirements",
            "is_open",
            "published_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]