from django.db import models
from datetime import datetime
from django.utils import timezone
import os, random
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice)(chars) for x in range(10))
    return f'profile_pic/{basefilename}_{randomstr}{file_extension}'


# --- System User model (for your own app users) ---
class SystemUser(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(max_length=100, verbose_name="Email")
    contact_number = models.CharField(max_length=15, verbose_name="Contact Number")
    username = models.CharField(max_length=100, verbose_name="Username", unique=True)
    password = models.CharField(max_length=100, verbose_name="Password")
    user_image = models.ImageField(upload_to=image_path, default='profile_pic/image.png')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    # 🔹 Position/Role field for future access control
    position = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Role or position for future access control"
    )

    def image_tag(self):
        return mark_safe(f'<img src="{self.user_image.url}" width="50" height="50" />')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} ({self.username})"


# --- UserProfile for Django's built-in User ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_image = models.ImageField(upload_to='profile_pic/', default='profile_pic/image.png', blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)  # Add this

    # 🔹 Position/Role field for future access control
    position = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Role or position for future access control"
    )

    def image_tag(self):
        if self.user_image:
            return mark_safe(f'<img src="{self.user_image.url}" width="50" height="50" />')
        return "(No Image)"

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ✅ Automatically create or update profile when user is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # Fixed from Profile -> UserProfile
    else:
        instance.profile.save()


# --- Category Model ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# --- InventoryItem Model ---
class InventoryItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    reorder_level = models.PositiveIntegerField(blank=True, null=True)
    maximum_level = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)