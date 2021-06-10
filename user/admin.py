from django.contrib import admin

from .models import CustomUser, AddressGlobal, UserProfile


admin.site.register((CustomUser, AddressGlobal, UserProfile,))