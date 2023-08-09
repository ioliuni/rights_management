from django.core.validators import MinLengthValidator
from django.db import models

from rights_management.accounts.models import only_lettars
from rights_management.department.models import Department
from rights_management.job_profile.models import Job_profile



class Work_people(models.Model):
    first_name = models.CharField(max_length=30, validators=[MinLengthValidator(2), only_lettars])
    last_name = models.CharField(max_length=30, validators=[MinLengthValidator(2), only_lettars])
    email=models.EmailField(unique=True)
    in_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True)
    with_job_profile=models.ManyToManyField(Job_profile, blank=True, null=True)
    owner=models.IntegerField(default=1)


    def __str__(self):
        return self.first_name+ " "+self.last_name