from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import SiteContent

admin.site.register(SiteContent, SingletonModelAdmin)
