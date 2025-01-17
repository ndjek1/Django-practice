from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'blood_type', 'alergies', 'spouse', 'last_hospitalisation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
             'age': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
              'gender': forms.Select(attrs={'class': 'form-select'}),
               'blood_type': forms.Select(attrs={'class': 'form-select'}, choices=[('A+','A+'), ('A-','A-'), ('B+','B+'), ('B-','B-'), ('AB+','AB+'), ('AB-','AB-'), ('O+','O+'), ('O-','O-')]),
               'alergies': forms.TextInput(attrs={'class': 'form-control'}),
               'spouse': forms.TextInput(attrs={'class': 'form-control'}),
               'last_hospitalisation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }