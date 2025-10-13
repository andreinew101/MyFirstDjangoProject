from django.shortcuts import redirect

def systemuser_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and 'system_user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
