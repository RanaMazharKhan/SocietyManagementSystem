"""
URL configuration for societymanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index, name='index'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path("admin_login/",views.admin_login,name="admin_login"),
    path("admin_dashboard/",views.admin_dashboard,name="admin_dashboard"),
    path("manage-requests/",views.manage_requests,name="manage_requests"),
    path("approve-request/<int:id>/",views.approve_request,name="approve_request"),
    path("complete-request/<int:id>/",views.complete_request,name="complete_request"),
    path("delete-request-admin/<int:id>/",views.delete_request_admin,name="delete_request_admin"),
    path("manage-announcements/",views.manage_announcements,name="manage_announcements"),
    path("delete-announcement/<int:id>/",views.delete_announcement,name="delete_announcement"),
    path("manage_users/",views.manage_users,name="manage_users"),
    path("delete-user/<int:id>/",views.delete_user,name="delete_user"),
    path('admin_logout/',views.admin_logout, name='admin_logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('create_request/', views.create_request, name='create_request'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('edit_request/<int:request_id>/', views.edit_request, name='edit_request'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('announcements/', views.announcements, name='announcements'),
    path('logout/',views.logout, name='logout'),
    path('send-email-all/', views.send_email_to_all_users, name='send_email_all'),
    path('activate/<int:user_id>/', views.activate_account, name='activate_account'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('password_reset_done/',views.password_reset_done,name='password_reset_done'),
    path('reset_password/<str:token>/',views.reset_password,name='reset_password'),
    path('password_reset_complete/',views.password_reset_complete,name='password_reset_complete'),

]
