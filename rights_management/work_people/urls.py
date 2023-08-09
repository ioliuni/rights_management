from django.urls import path

from rights_management.work_people import views

urlpatterns=[
    path('add/', views.work_people_add, name='work_people_add'),
    path('list/', views.work_people_list.as_view(), name='work_people_list'),
    path('detail/<int:pk>/', views.work_people_details.as_view(), name='work_people_details'),
    path('edit/<int:pk>/', views.work_people_edit.as_view(), name='work_people_edit'),
    path('delete/<int:pk>/', views.work_people_delete, name='work_people_delete'),
]