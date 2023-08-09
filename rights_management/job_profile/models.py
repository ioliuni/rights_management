from django.db import models

from rights_management.access_rights.models import Access_rights
from rights_management.department.models import Department

def get_depar():
    return print(Department.objects.all().first().id)

class Job_profile(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    job_access=models.ManyToManyField(Access_rights, null=True, blank=True)
    owner=models.IntegerField(default=1)
    in_department=models.ForeignKey(Department, on_delete=models.DO_NOTHING,  default=1, null=True, blank=True)

    def __str__(self):
        return self.name



