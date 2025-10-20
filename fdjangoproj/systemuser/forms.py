from django import forms
from .models import SystemUser, InventoryItem, Category
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# -------------------- Add User Form --------------------
class SystemUserAddForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'username',
            'user_image',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set default password or leave blank
        if not user.pk:
            user.password = make_password('defaultpassword123')  # or leave empty
        if commit:
            user.save()
        return user
    
# -------------------- Edit Profile Form --------------------
class SystemUserForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter current password'}),
        label="Current Password",
        required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password (leave blank to keep current)'}),
        label="New Password",
        required=False
    )

    class Meta:
        model = SystemUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'username',
            'user_image',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.password = make_password(new_password)  # hash the new password
        if commit:
            user.save()
        return user
    
# -------------------- Admin Profile Form --------------------
class AdminProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter current password'}),
        label="Current Password"
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password (optional)'}),
        label="New Password (leave blank to keep current)"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'maximum_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Adjust this based on your actual model field name
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'  # Include all fields in the model

class InventoryReportForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )