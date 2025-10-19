from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import SystemUser, InventoryItem, Category
from .forms import AdminProfileForm

# --- Django's built-in User Admin (Admin Profile) ---
class CustomUserAdmin(UserAdmin):
    form = AdminProfileForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# --- SystemUser Admin ---
@admin.register(SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'contact_number',
        'username',
        'created_at',
    )
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# --- InventoryItem Admin ---
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_id',
        'item_name',
        'description',
        'category',
        'quantity',
        'price',
        'supplier',
        'reorder_level',
        'maximum_level',
        'date_added',
        'date_modified',
    )
    search_fields = ('item_name', 'supplier')
    list_filter = ('category',)


# --- Category Admin ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
