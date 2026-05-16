from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.cms.models import Page

from .serializers import  PublicPageSerializer

class PublicPageDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, slug):
        page = get_object_or_404(
            Page.objects.prefetch_related("sections"),
            slug=slug,
            is_published=True,
        )

        page.sections.set(
            page.sections.filter(is_active=True).order_by("sort_order", "id")
        )

        serializer = PublicPageSerializer(
            page,
            context={"request": request},
        )
        return Response(serializer.data)


class PublicHomeView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        page = get_object_or_404(
            Page.objects.prefetch_related("sections"),
            slug="home",
            is_published=True,
        )

        page.sections.set(
            page.sections.filter(is_active=True).order_by("sort_order", "id")
        )

        serializer = PublicPageSerializer(
            page,
            context={"request": request},
        )
        return Response(serializer.data)

