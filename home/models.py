from django.db import models # type: ignore

# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    blood_type = models.CharField(max_length=3)
    alergies = models.CharField(max_length=300)
    spouse = models.CharField(max_length=100)
    last_hospitalisation = models.DateField()



class Doctor(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=[('F','Female'), ('M','Male')])
    blood_type = models.CharField(max_length=3)
    specialization = models.CharField(max_length=100)
