from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SystemUser
from .forms import SystemUserForm


# 🔹 LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # go to dashboard after login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'systemuser/login.html')


# 🔹 LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')


# 🔹 DASHBOARD (requires login)
@login_required(login_url='login')
def index(request):
    return render(request, 'systemuser/index.html')


# 🔹 USER LIST (requires login)
@login_required(login_url='login')
def userlist(request):
    user_list = SystemUser.objects.all()
    context = {'user_list': user_list}
    return render(request, 'systemuser/userlist.html', context)


# 🔹 ADD USER (requires login)
@login_required(login_url='login')
def adduser(request):
    if request.method == "POST":
        form = SystemUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userlist')
    else:
        form = SystemUserForm()
    return render(request, 'systemuser/adduser.html', {'form': form})
