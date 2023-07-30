from django.urls import path

from rights_management.job_profile import views

urlpatterns=[
    path('add/', views.job_profile_add, name='job_profile_add'),
    path('list/', views.job_profile_list.as_view(), name='job_profile_list'),
    path('detail/<int:pk>/', views.job_profile_details.as_view(), name='job_profile_details'),
    path('edit/<int:pk>/', views.job_profile_edit.as_view(), name='job_profile_edit'),
    path('delete/<int:pk>/', views.job_profile_delete, name='job_profile_delete'),
]