from django.contrib import admin

from rights_management.job_profile.models import Job_profile


# Register your models here.
@admin.register(Job_profile)
class Job_profileAdmin(admin.ModelAdmin):
    list_display = ['name', 'in_department','get_access_rights' ]
    list_filter = ['in_department']
    search_fields = ['name']
    ordering = [ 'in_department']
    #fields = [('name', 'in_department'), 'description', 'job_access']
    fieldsets = (
        ('Profile info',
         {'fields': ('name', 'in_department', 'description')}),
        ('Access rigths in Profile',
         {'fields': ('job_access',), }),
    )

    @staticmethod
    def get_access_rights(obj):
        return ", ".join(([j.right_name for j in obj.job_access.all()]))

