from systemuser.models import SystemUser

def user_position(request):
    """Add user position information to template context."""
    position = None
    is_admin_or_manager = False

    if request.user.is_authenticated:
        # Django user - automatically admin
        position = 'Admin'
        is_admin_or_manager = True
    elif 'system_user_id' in request.session:
        try:
            system_user = SystemUser.objects.get(id=request.session['system_user_id'])
            position = system_user.position
            is_admin_or_manager = position in ['Admin', 'Manager']
        except SystemUser.DoesNotExist:
            pass

    return {
        'user_position': position,
        'is_admin_or_manager': is_admin_or_manager,
    }
