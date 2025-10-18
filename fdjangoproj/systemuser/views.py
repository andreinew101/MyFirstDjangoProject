from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import SystemUser, InventoryItem, Category
from .forms import SystemUserForm, InventoryItemForm, CategoryForm
from .decorators import systemuser_login_required

from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.db import models
from django.db.models import Sum

# 🔹 LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 1️⃣ Try authenticating a Django built-in user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')
        # 2️⃣ If not found, check SystemUser model
        try:
            system_user = SystemUser.objects.get(username=username)
            
            # For plain text passwords:
            if system_user.password == password:
                request.session['system_user_id'] = system_user.id
                request.session['system_user_name'] = system_user.username
                messages.success(request, f"Welcome back, {system_user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid password.")

        except SystemUser.DoesNotExist:
            messages.error(request, "Username not found.")

    return render(request, 'systemuser/login.html')


# 🔹 LOGOUT VIEW
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    request.session.flush()
    return redirect('login')


# 🔹 COMBINED LOGIN PROTECTION DECORATOR
def combined_login_required(view_func):
    """Allow access if Django user is logged in or SystemUser session exists."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and 'system_user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# 🔹 DASHBOARD (requires login)
def index(request):
    total_items = InventoryItem.objects.count()
    low_stock_count = InventoryItem.objects.filter(quantity__lte=models.F('reorder_level')).count()
    out_of_stock_count = InventoryItem.objects.filter(quantity=0).count()
    supplier_count = InventoryItem.objects.values('supplier').distinct().count()

    context = {
        'total_items': total_items,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'supplier_count': supplier_count,
    }
    return render(request, 'systemuser/index.html', context)

# 🔹 USER LIST (requires login)
@combined_login_required
def userlist(request):
    user_list = SystemUser.objects.all()
    context = {'user_list': user_list}
    return render(request, 'systemuser/userlist.html', context)


# 🔹 ADD USER (requires login)
@combined_login_required
def adduser(request):
    if request.method == "POST":
        form = SystemUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userlist')
    else:
        form = SystemUserForm()
    return render(request, 'systemuser/adduser.html', {'form': form})


#============================= INVENTORY ITEMS ==========================

# 🔹 Inventory List View
@combined_login_required    
def item_list(request):
    items = InventoryItem.objects.all().order_by('-item_id')  # changed from '-id'
    return render(request, 'systemuser/item_list.html', {'items': items})

# 🔹 Add Item View
@combined_login_required
def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = InventoryItemForm()
    return render(request, 'systemuser/add_item.html', {'form': form})

# 🔹 Edit Item View
@combined_login_required
def edit_item(request, pk):
    item = get_object_or_404(InventoryItem, item_id=pk)  # changed from pk=pk
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'systemuser/edit_item.html', {'form': form, 'item': item})


# 🔹 Add Category View
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_item')  # Go back to Add Item page
    else:
        form = CategoryForm()
    return render(request, 'systemuser/add_category.html', {'form': form})

#=================================================================================

@combined_login_required
def delete_item(request, pk):
    item = get_object_or_404(InventoryItem, item_id=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('item_list')
    return render(request, 'systemuser/confirm_delete.html', {'item': item})

from django.db.models import Sum
from .models import InventoryItem  # make sure this import exists

@combined_login_required
def index(request):
    # 📦 Compute key stats
    total_items = InventoryItem.objects.count()
    total_quantity = InventoryItem.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    low_stock_count = InventoryItem.objects.filter(quantity__lte=10).count()
    out_of_stock_count = InventoryItem.objects.filter(quantity=0).count()
    supplier_count = InventoryItem.objects.values('supplier').distinct().count()

    # 🧮 Compute dynamic maximum storage capacity
    max_capacity = InventoryItem.objects.aggregate(Sum('maximum_level'))['maximum_level__sum'] or 0

    # 🟩 Compute storage usage based on total quantities
    storage_used_percentage = round((total_quantity / max_capacity) * 100, 2) if max_capacity > 0 else 0

    context = {
        'total_items': total_items,
        'total_quantity': total_quantity,  # sum of all quantities
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'supplier_count': supplier_count,
        'max_capacity': max_capacity,      # sum of all max levels
        'storage_used_percentage': storage_used_percentage,
    }

    return render(request, 'systemuser/index.html', context)
