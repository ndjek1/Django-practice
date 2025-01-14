from django.shortcuts import render, redirect # type: ignore

from home.models import *
from django.http import HttpResponse
from django.db.models import Q # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore # Import the function to 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def add_patient(request):

    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        blood_type = request.POST['blood_type']
        alergies = request.POST['alergies']
        spouse = request.POST['spouse']
        last_hospitalisation = request.POST['last_hospitalisation']


        patient = Patient(
            name=name,
            age=age,
            gender=gender,
            blood_type=blood_type,
            alergies=alergies,
            spouse=spouse,
            last_hospitalisation=last_hospitalisation,
        )

        patient.save()
        return redirect('patients_list') # Replace 'success_page' with your success URL

    return render(request, 'add_patient_record.html') # Render the html template

def success_page(request):
    return render(request, "success_page.html") # Replace with your success message HTML template.



@login_required
def patients_list(request):
    search_term = request.GET.get('search', '')
    
    if search_term:
         patients = Patient.objects.filter(
            Q(name__icontains=search_term) | Q(blood_type__icontains=search_term), # Search in name and blood_type
        ) 
    else:
        patients = Patient.objects.all()
    
    context = {
        'patients': patients,
        'search_term': search_term
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