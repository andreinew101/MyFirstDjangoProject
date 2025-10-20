from django.shortcuts import redirect
from .models import SystemUser

def systemuser_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and 'system_user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_manager_required(view_func):
    """Allow access only to Django users or SystemUsers with position Admin or Manager."""
    def wrapper(request, *args, **kwargs):
        # Django user is automatically admin
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # Check SystemUser position
        if 'system_user_id' in request.session:
            try:
                system_user = SystemUser.objects.get(id=request.session['system_user_id'])
                if system_user.position in ['Admin', 'Manager']:
                    return view_func(request, *args, **kwargs)
            except SystemUser.DoesNotExist:
                pass

        return redirect('login')
    return wrapper
