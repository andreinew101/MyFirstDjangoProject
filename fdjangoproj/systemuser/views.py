from django.shortcuts import render
from django.http import HttpResponse
from .models import SystemUser
from .forms import SystemUserForm
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'systemuser/index.html')

def userlist(request):
    user_list = SystemUser.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'systemuser/userlist.html', context)

def adduser(request):
    if request.method == "POST":
        form = SystemUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userlist')  # or wherever you want to go after saving
    else:
        form = SystemUserForm()
    
    # ✅ Always return something
    return render(request, 'systemuser/adduser.html', {'form': form})