from django import forms

from rights_management.job_profile.models import Job_profile


class Job_profileForm(forms.ModelForm):
    class Meta:
        model=Job_profile
        #fields = '__all__'
        fields = [ 'name', 'description', 'job_access']
        # widgets = {
        #     "description": forms.Textarea(),
        #     #"job_access": forms.SelectMultiple()
        #     #"job_access": forms.CheckboxSelectMultiple()
        # }


class Job_profileDeleteForm(Job_profileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'