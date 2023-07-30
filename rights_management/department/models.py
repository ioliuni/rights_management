from django.db import models

from rights_management.accounts.models import RightsUser

class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    user = models.ManyToManyField(RightsUser, related_name="access_rights")

    def __str__(self):
        return self.name
