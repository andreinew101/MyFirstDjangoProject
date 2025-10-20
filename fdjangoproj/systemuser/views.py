from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
#from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import SystemUser, InventoryItem, Category, InventoryItem
from .forms import SystemUserForm, InventoryItemForm, CategoryForm, InventoryReportForm, AdminProfileForm
from .decorators import systemuser_login_required, admin_manager_required

from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.db import models
from django.db.models import Sum, Count, F



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


# 🔹 USER LIST (requires admin/manager)
@admin_manager_required
def userlist(request):
    user_list = SystemUser.objects.all()
    context = {'user_list': user_list}
    return render(request, 'systemuser/userlist.html', context)


# 🔹 ADD USER (requires admin/manager)
@admin_manager_required
def adduser(request):
    if request.method == "POST":
        form = SystemUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userlist')
    else:
        form = SystemUserForm()

    # Restrict position choices: only Admins can set Admin position
    if not request.user.is_authenticated:
        # SystemUser - check if Admin
        try:
            current_user = SystemUser.objects.get(id=request.session['system_user_id'])
            if current_user.position != 'Admin':
                # Remove Admin choice
                form.fields['position'].choices = [
                    choice for choice in form.fields['position'].choices
                    if choice[0] != 'Admin'
                ]
        except SystemUser.DoesNotExist:
            pass
    # Django users can choose all positions

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

@combined_login_required
def edit_profile(request):
    # Determine if the user is a Django admin or a SystemUser
    if request.user.is_authenticated:
        is_admin = True
        user_obj = request.user
        FormClass = AdminProfileForm
    else:
        is_admin = False
        system_user_id = request.session.get('system_user_id')
        user_obj = get_object_or_404(SystemUser, id=system_user_id)
        FormClass = SystemUserForm

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=user_obj)
        current_password = request.POST.get('current_password')

        # Verify password correctness
        if is_admin:
            password_correct = user_obj.check_password(current_password)
        else:
            password_correct = (user_obj.password == current_password)

        if not password_correct:
            messages.error(request, "❌ Incorrect current password. Please try again.")
        elif form.is_valid():
            updated_user = form.save(commit=False)

            # Handle password change
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                if is_admin:
                    user_obj.set_password(new_password)
                    update_session_auth_hash(request, user_obj)  # Keeps admin logged in
                else:
                    user_obj.password = new_password  # plaintext for now

            updated_user.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect('edit_profile')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = FormClass(instance=user_obj)

    context = {
        'form': form,
        'is_admin': is_admin,
        'user_obj': user_obj,
    }
    return render(request, 'systemuser/edit_profile.html', context)

#=====================Login and others:=======================================

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
    total_items = InventoryItem.objects.count()
    low_stock_items = InventoryItem.objects.filter(quantity__lte=F('reorder_level')).count()
    out_of_stock_items = InventoryItem.objects.filter(quantity=0).count()
    category_count = Category.objects.count()

    # Calculate total quantity and storage usage
    total_quantity = InventoryItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
    max_capacity = InventoryItem.objects.aggregate(total=Sum('maximum_level'))['total'] or 0
    storage_used_percentage = (total_quantity / max_capacity) * 100 if max_capacity > 0 else 0

    # Category distribution (for donut chart)
    category_data = []
    categories = Category.objects.all()
    total_quantity = InventoryItem.objects.aggregate(total=Sum('quantity'))['total'] or 0

    # Generate evenly spaced distinct hues (based on number of categories)
    for i, category in enumerate(categories):
        total_in_cat = InventoryItem.objects.filter(category=category).aggregate(total=Sum('quantity'))['total'] or 0
        percentage = round((total_in_cat / total_quantity) * 100, 2) if total_quantity > 0 else 0
        
        hue = int((i * 360) / max(len(categories), 1))  # Spread colors across the hue wheel
        color = f"hsl({hue}, 70%, 50%)"
        
        category_data.append({
            "name": category.name,
            "percentage": percentage,
            "color": color
        })

    context = {
        "total_items": total_items,
        "low_stock_items": low_stock_items,
        "out_of_stock_items": out_of_stock_items,
        "category_count": category_count,
        "storage_used_percentage": round(storage_used_percentage, 2),
        "total_quantity": total_quantity,
        "max_capacity": max_capacity,
        "category_data": category_data,
    }
    return render(request, "systemuser/index.html", context)

@combined_login_required
def inventory_report(request):
    from django.db.models import Sum

    form = InventoryReportForm(request.GET or None)
    items = InventoryItem.objects.all().order_by('-date_added')

    # Apply filters
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        category = form.cleaned_data.get('category')

        if start_date:
            items = items.filter(date_added__gte=start_date)
        if end_date:
            items = items.filter(date_added__lte=end_date)
        if category:
            items = items.filter(category=category)

    # Totals
    total_value = sum(item.quantity * item.price for item in items)
    total_quantity = items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    context = {
        'form': form,
        'items': items,
        'total_value': total_value,
        'total_quantity': total_quantity,
    }
    return render(request, 'systemuser/inventory_report.html', context)