from django.db import models # type: ignore
from datetime import date


class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    blood_type = models.CharField(max_length=3)
    alergies = models.CharField(max_length=300)
    spouse = models.CharField(max_length=100)
    last_hospitalisation = models.DateField()
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None  # Return None if date_of_birth is not provided



class Doctor(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=[('F','Female'), ('M','Male')])
    blood_type = models.CharField(max_length=3)
    specialization = models.CharField(max_length=100)
