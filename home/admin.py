from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string  # To generate a random password
from django.contrib import admin

from home.models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'blood_type', 'specialization')
    search_fields = ('name', 'specialization')

    def save_model(self, request, obj, form, change):
        """Create a User when a new Doctor is added from the admin panel"""
        if not change:  # Only for new entries
            username = obj.name.lower().replace(" ", "_")  # Generate a username
            password = get_random_string(10)  # Generate a random password

            user = User.objects.create_user(
                username=username,
                password=password
            )
            obj.user = user  # Assign the user to the doctor model

        super().save_model(request, obj, form, change)
admin.site.register(Doctor, DoctorAdmin)