from django.shortcuts import render, redirect, get_object_or_404 # type: ignore

from home.models import *
from django.http import HttpResponse
from django.db.models import Q # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore # Import the function to 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.


def add_patient(request):
     if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('patients_list')
     else:
        form = PatientForm()
 
     return render(request, 'add_patient_record.html', {'form': form})

def success_page(request):
    return render(request, "success_page.html") # Replace with your success message HTML template.



@login_required
def patients_list(request):
    total_patients = Patient.objects.count()
    male_patients = Patient.objects.filter(gender='M').count()
    female_patients = Patient.objects.filter(gender='F').count()
    search_term = request.GET.get('search', '')
    if search_term:
        patients = Patient.objects.filter(
           Q(name__icontains=search_term) | Q(blood_type__icontains=search_term)
        )
    else:
       patients = Patient.objects.all()
    
    context = {
            'total_patients': total_patients,
            'male_patients': male_patients,
            'female_patients': female_patients,
            'patients': patients,
            'search_term':search_term,
        }
    return render(request, 'patients_list.html', context)


def doctor_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        blood_type = request.POST['blood_type']
        specialization = request.POST['specialization']
        username = request.POST['username']
        password = request.POST['password']

        # Hash the password
        hashed_password = make_password(password)

        # Create a new user for login
        user = User.objects.create(username=username, password=hashed_password)

        # Create a new doctor with the same name and other data
        Doctor.objects.create(
            name=name,
            gender=gender,
            blood_type=blood_type,
            specialization=specialization
        )
        return redirect('success_page')  # Replace 'success_page' with your success URL
    return render(request, 'doctor_register.html')

def edit_patient_record(request, patient_id):
 
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        patient.name = request.POST['name']
        patient.alergies = request.POST['alergies']
        patient.blood_type = request.POST['blood_type']
        patient.alergies = request.POST['alergies']
        patient.spouse = request.POST['spouse']
        patient.last_hospitalisation = request.POST['last_hospitalisation']
        patient.save()
        return redirect('patients_list')
    
    return render(request, 'edit_record.html', {'patient': patient})
    
def delete_patient_record(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.delete()
    return redirect('patients_list')

def user_login(request):
    error_message = None  # Initialize error_message to None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('patients_list')  # Replace 'dashboard' with your success URL

        else:
            error_message = "Invalid username or password"

    return render(request, 'login.html', {'error_message': error_message})

def user_logout(request):
    if request.method == 'POST':
        logout(request) # pass the request object to the logout method
        return redirect('login') # Corrected redirect name
    return redirect('login')  # Redirect to login page if not a POST request