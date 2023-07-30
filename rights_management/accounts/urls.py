from django.urls import path, include

from rights_management.accounts import views

urlpatterns =[
    path('register/', views.user_register_add, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    ]