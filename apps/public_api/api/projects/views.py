from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from apps.cms.models.projects import Project, ProjectSection
from .serializers import PublicProjectSerializer


class PublicProjectDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, slug):
        project = get_object_or_404(
            Project.objects.prefetch_related(
                Prefetch(
                    "sections",
                    queryset=ProjectSection.objects.filter(is_active=True).order_by(
                        "sort_order",
                        "id",
                    ),
                )
            ),
            slug=slug,
            is_published=True,
        )

        serializer = PublicProjectSerializer(
            project,
            context={"request": request},
        )
        return Response(serializer.data)


class PublicProjectListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        projects = (
            Project.objects.filter(is_published=True)
            .order_by("sort_order", "title")
        )

        serializer = PublicProjectSerializer(
            projects,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)