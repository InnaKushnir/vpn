from django.contrib import admin

from .models import Site, SiteTransition

admin.site.register(Site)
admin.site.register(SiteTransition)
