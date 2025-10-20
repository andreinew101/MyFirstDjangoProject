from django.shortcuts import redirect
from django.contrib import messages
from systemuser.models import SystemUser

def systemuser_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and 'system_user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_or_manager_required(view_func):
    """
    Decorator to restrict access to users with position 'Admin' or 'Manager'.
    Works for both Django built-in users and SystemUsers.
    """
    def wrapper(request, *args, **kwargs):
        # First check if user is logged in
        if not request.user.is_authenticated and 'system_user_id' not in request.session:
            return redirect('login')

        # Get user position
        position = None
        if request.user.is_authenticated:
            # For Django built-in User
            position = getattr(request.user.profile, 'position', None)
        elif 'system_user_id' in request.session:
            # For SystemUser
            try:
                system_user = SystemUser.objects.get(id=request.session['system_user_id'])
                position = system_user.position
            except SystemUser.DoesNotExist:
                pass

        # Check if position is Admin or Manager
        if position not in ['Admin', 'Manager']:
            messages.error(request, "Access denied. Only Admin or Manager can access this page.")
            return redirect('index')  # Redirect to dashboard

        return view_func(request, *args, **kwargs)
    return wrapper
