from django.urls import path
from . import views

urlpatterns = [
    # Default route → login page
    path('', views.login_view, name='login'),

    # Dashboard and main pages
    path('dashboard/', views.index, name='index'),
    path('users/', views.userlist, name='userlist'),
    path('adduser/', views.adduser, name='adduser'),

    # Optional or legacy route (you can remove this if not used)
    path('adduser/index.html', views.adduser, name='adduser_index'),
    
    # Logout route
    path('logout/', views.logout_view, name='logout'),
]
