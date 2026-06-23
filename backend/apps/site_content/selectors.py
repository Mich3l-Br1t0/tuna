from .models import SiteContent


def site_content_get() -> SiteContent:
    return SiteContent.get_solo()
