from django.db import models
from datetime import datetime
from django.utils import timezone
import os, random
from django.utils.html import mark_safe

now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice)(chars) for x in range(10))
    _now = datetime.now()

    return r'profile_pic\{basename}_{randomstring}{ext}'.format(basename=basefilename, randomstring=randomstr, ext=file_extension)

class SystemUser(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(max_length=100, verbose_name="Email")
    contact_number = models.CharField(max_length=15, verbose_name="Contact Number")
    username = models.CharField(max_length=100, verbose_name="Username", unique=True)
    password = models.CharField(max_length=100, verbose_name="Password")
    user_image = models.ImageField(upload_to=image_path, default='profile_pic/image.png')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def image_tag(self):
        return mark_safe(f'<img src="{self.user_image.url}" width="50" height="50" />')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} ({self.username})"
    
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


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
    


