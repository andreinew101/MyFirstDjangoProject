from django.contrib import admin
from .models import SystemUser

class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_number', 'username', 'image_tag', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(SystemUser, SystemUserAdmin)
