from django.contrib import admin
from .models import SystemUser, InventoryItem, Category

# --- SystemUser Admin ---
class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_number', 'username', 'image_tag', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(SystemUser, SystemUserAdmin)

# --- InventoryItem Admin ---
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'item_name', 'category', 'quantity', 'price', 'date_added', 'date_modified')
    search_fields = ('item_name', 'category__name')  # FK requires double underscore
    list_filter = ('category', 'date_added')
    ordering = ('item_id',)  # Descending by ID

admin.site.register(InventoryItem, InventoryItemAdmin)

# --- Category Admin ---
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)