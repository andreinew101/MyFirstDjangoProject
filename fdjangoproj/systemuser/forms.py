from django import forms
from .models import SystemUser

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
            'password': forms.PasswordInput(),  # hides password text
        }