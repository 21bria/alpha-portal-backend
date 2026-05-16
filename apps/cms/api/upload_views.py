from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage

class TinyMCEImageUploadView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]

    upload_folder = "news/content"

    def post(self, request):
        image = request.FILES.get("file")

        if not image:
            return Response({"detail": "No image uploaded"}, status=400)

        path = default_storage.save(
            f"{self.upload_folder}/{image.name}",
            image
        )

        url = request.build_absolute_uri(default_storage.url(path))

        return Response({
            "location": url
        })


class TinyMCEImageUploadSectionsView(TinyMCEImageUploadView):
    upload_folder = "sections/content"

# Project Image
class TinyMCEProjectImageUploadView(TinyMCEImageUploadView):
    upload_folder = "projects/content"

class TinyMCEProjectSectionImageUploadView(TinyMCEImageUploadView):
    upload_folder = "projects/sections/content"