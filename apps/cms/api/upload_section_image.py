import os
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_section_image(request):
    file = request.FILES.get("file")
    folder = request.data.get("folder", "general")

    if not file:
        return Response(
            {"detail": "No file uploaded"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    safe_folder = folder.replace("/", "").replace("\\", "")
    path = f"pages/sections/{safe_folder}/{file.name}"

    saved_path = default_storage.save(path, file)

    url = request.build_absolute_uri(
        default_storage.url(saved_path)
    )

    return Response({
        "url": url,
    })