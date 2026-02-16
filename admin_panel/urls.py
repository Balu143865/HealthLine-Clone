"""
Admin Panel URLs
"""
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('stats/', views.dashboard_stats, name='stats'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<slug:slug>/edit/', views.category_edit, name='category_edit'),
    path('categories/<slug:slug>/delete/', views.category_delete, name='category_delete'),
    
    # Articles
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<slug:slug>/edit/', views.article_edit, name='article_edit'),
    path('articles/<slug:slug>/delete/', views.article_delete, name='article_delete'),
    
    # Newsletters
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/<int:pk>/toggle/', views.newsletter_toggle, name='newsletter_toggle'),
    path('newsletters/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/toggle-staff/', views.user_toggle_staff, name='user_toggle_staff'),
    
    # API
    path('api/subcategories/', views.get_subcategories, name='get_subcategories'),
]