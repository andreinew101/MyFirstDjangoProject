from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Authentication
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🔹 Dashboard and users
    path('dashboard/', views.index, name='index'),
    path('users/', views.userlist, name='userlist'),
    path('adduser/', views.adduser, name='adduser'),

    # 🔹 Inventory
    path('inventory/', views.item_list, name='item_list'),
    path('inventory/add/', views.add_item, name='add_item'),
    path('inventory/edit/<int:pk>/', views.edit_item, name='edit_item'),
    
    # Logout route
    path('logout/', views.logout_view, name='logout'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('inventory/', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:pk>/', views.edit_item, name='edit_item'),

    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('categories/add/', views.add_category, name='add_category'), 
]


