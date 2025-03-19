from django.urls import path, include
from . import views


urlpatterns = [
    path('new_patient/', views.add_patient, name='patient'),
    path('success_page/', views.success_page, name='success_page'),
    path('', views.patients_list, name='patients_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/<int:patient_id>/', views.edit_patient_record, name='edit_patient_record'), # Add this line to your urls.py file.
     path('delete/<int:patient_id>/', views.delete_patient_record, name='delete_patient_record'),
]