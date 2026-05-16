from rest_framework.views import APIView
from rest_framework.response import Response

from apps.cms.models import CompanyProfile
from .serializers import PublicCompanyProfileSerializer

class PublicCompanyProfileView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        profile = CompanyProfile.objects.first()

        if not profile:
            return Response({})

        serializer = PublicCompanyProfileSerializer(
            profile,
            context={"request": request},
        )

        return Response(serializer.data)