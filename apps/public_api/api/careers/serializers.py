# apps/cms/api/public/careers/serializers.py

from rest_framework import serializers
from apps.cms.models import JobVacancy


class PublicJobVacancySerializer(serializers.ModelSerializer):
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
        ]