from django.db import models

from rights_management.access_rights.models import Access_rights


class Job_profile(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    job_access=models.ManyToManyField(Access_rights)

    def __str__(self):
        pass

# Create your models here.
