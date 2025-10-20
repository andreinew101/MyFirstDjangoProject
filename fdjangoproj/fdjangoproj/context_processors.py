from systemuser.models import SystemUser

def user_position(request):
    """
    Context processor to add user position to template context.
    """
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
    return {'user_position': position}
