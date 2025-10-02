from django.shortcuts import render
from django.http import HttpResponse
from .models import SystemUser

# Create your views here.

def index(request):
    return render(request, 'systemuser/index.html')

def userlist(request):
    user_list = SystemUser.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'systemuser/userlist.html', context)