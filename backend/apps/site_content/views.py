from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import SiteContent
from .serializers import SiteContentSerializer


class SiteContentView(RetrieveAPIView):
    """Public, read-only home-page content (the single SiteContent row)."""

    permission_classes = [AllowAny]
    serializer_class = SiteContentSerializer

    def get_object(self) -> SiteContent:
        return SiteContent.get_solo()
