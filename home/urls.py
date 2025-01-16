from django.urls import path, include
from . import views


urlpatterns = [
    path('new_patient/', views.add_patient, name='patient'),
    path('success_page/', views.success_page, name='success_page'),
    path('', views.patients_list, name='patients_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('doctor_register/', views.doctor_register, name='doctor_register'),  # Add this line to your urls.py file.
    # path('inventories/', include('inv_management.urls')),
]