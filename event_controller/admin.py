from django.contrib import admin

from .models import EventMain, EventFeature, EventAttender, Cat


admin.site.register((EventMain, EventFeature, EventAttender, Cat))