from django.contrib.auth.models import Permission
from django.core.validators import MinValueValidator
from django.db import models

from rights_management.accounts.models import RightsUser

TYPE=[
    ("Accounting Software","Accounting Software"),
    ("Human Resources","Human Resources"),
    ("Customer management","Customer management"),
    ("Design software","Design software"),
    ("Production management", "Production management"),
    ("Inventory management","Inventory management"),
]



class Access_rights(models.Model):
    right_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    software = models.CharField(max_length=30, choices=TYPE)
    user = models.ManyToManyField(RightsUser, related_name="access_rights")
    def __str__(self):
        return self.right_name

class View_permission(models.Model):
    view_name=models.CharField(max_length=30, unique=True)
    with_permission=models.OneToOneField(Permission, on_delete=models.DO_NOTHING)