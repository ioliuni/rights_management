from django.urls import path

from rights_management.access_rights import views

urlpatterns=[
    path('add/', views.access_rights_add, name='access_rights_add'),
    path('list/', views.access_rights_list.as_view(), name='access_rights_list'),
    path('detail/<int:pk>/', views.access_rights_details.as_view(), name='access_rights_details'),
    path('edit/<int:pk>/', views.access_rights_edit.as_view(), name='access_rights_edit'),
    path('delete/<int:pk>/', views.access_rights_delete, name='access_rights_delete'),
]

