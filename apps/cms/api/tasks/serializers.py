# apps/cms/api/tasks/serializers.py

from rest_framework import serializers
from apps.cms.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "code",
            "title",
            "slug",
            "description",
            "location",
            "department",
            "status",
            "priority",
            "assigned_to",
            "start_date",
            "due_date",
            "checklist",
            "attachments",
            "is_public",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "code",
            "slug",
            "created_at",
            "updated_at",
        ]