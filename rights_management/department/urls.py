from django.urls import path

from rights_management.department import views

urlpatterns=[
    path('add/', views.department_add, name='department_add'),
    path('list/', views.department_list.as_view(), name='department_list'),
    path('detail/<int:pk>/', views.department_details.as_view(), name='department_details'),
    path('edit/<int:pk>/', views.department_edit.as_view(), name='department_edit'),
    path('delete/<int:pk>/', views.department_delete, name='department_delete'),
    path('report/', views.report.as_view(), name='report'),
    path('people_in_department/<int:pk>', views.people_in_department.as_view(), name='people_in_department'),
    path('profile_in_department/<int:pk>', views.profile_in_department.as_view(), name='profile_in_department'),
    path('access_rights_in_profile/', views.access_rights_in_profile.as_view(), name='access_rights_in_profile'),
]
