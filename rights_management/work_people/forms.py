from django import forms

from rights_management.work_people.models import Work_people


class Work_peopleForm(forms.ModelForm):
    class Meta:
        model=Work_people
        #fields = '__all__'
        #fields = [ 'first_name', 'last_name', 'email', 'in_department', 'with_job_profile']
        fields = [ 'first_name', 'last_name', 'email', 'in_department']
