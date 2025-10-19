from django import forms
from .models import SystemUser, InventoryItem, Category
from django.contrib.auth.hashers import make_password

class SystemUserForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'username',
            'password',
            'user_image',       
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

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