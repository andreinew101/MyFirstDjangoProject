from django.contrib import admin
from .models import SystemUser, InventoryItem

class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_number', 'username', 'image_tag', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(SystemUser, SystemUserAdmin)

from django.contrib import admin
from .models import InventoryItem

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'item_name', 'category', 'quantity', 'price', 'supplier', 'reorder_level', 'maximum_level', 'date_added', 'date_modified')
    search_fields = ('item_name', 'category', 'supplier')
    list_filter = ('category', 'supplier', 'date_added')
    ordering = ('-date_added',)

admin.site.register(InventoryItem, InventoryItemAdmin)
