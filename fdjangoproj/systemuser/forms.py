from django import forms
from .models import SystemUser, InventoryItem, Category
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class SystemUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Position choices will be restricted in the view based on current user permissions
        # For new users, password is required
        # For existing users, password is optional (leave blank to keep current)
        if self.instance and self.instance.pk:
            # Editing existing user - make password optional
            self.fields['password'].required = False
            self.fields['password'].label = "New Password (leave blank to keep current)"
            self.fields['password'].widget.attrs['placeholder'] = 'Enter new password (leave blank to keep current)'

    class Meta:
        model = SystemUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'username',
            'position',
            'user_image',  # Notice: removed 'password' here
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        # Handle password for new users or password changes
        raw_password = self.cleaned_data.get('password')
        if raw_password:
            # For new users or when password is provided, set it
            user.password = raw_password  # Store as plain text as per existing system
        if commit:
            user.save()
        return user


    
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

class UpdateStockForm(forms.Form):
    quantity_change = forms.IntegerField(
        label="Quantity Change",
        help_text="Enter positive number to add stock, negative to subtract.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10 or -5'})
    )

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
