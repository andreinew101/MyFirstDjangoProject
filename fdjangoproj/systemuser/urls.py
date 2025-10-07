from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.userlist, name='userlist'),
    path('adduser/', views.adduser, name='adduser'),
    path('adduser/index.html', views.adduser, name='adduser_index'),
]