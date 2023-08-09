from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django import forms

from rights_management.department.models import Department


def only_lettars(value):
    if not value.isalpha():
        raise forms.ValidationError("Name should contain only letters!")

def get_depar():
    return Department.objects.get(id=1).id
class RightsUser(AbstractUser):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=30, validators=(validators.MinLengthValidator(2),only_lettars))
    last_name=models.CharField(max_length=30, validators=(validators.MinLengthValidator(2),only_lettars))
    #department=models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=get_depar, null=True, blank=True)

    def get_user_name(self):
        if self.first_name and self.last_name:
            return self.first_name+" "+self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.username

