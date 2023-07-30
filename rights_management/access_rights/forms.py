from django import forms

from rights_management.access_rights.models import Access_rights


class AccessForm(forms.ModelForm):
    class Meta:
        model = Access_rights
        fields = '__all__'
        exclude=['user',]
        widgets = {
            "description":forms.Textarea(),
        }

class AccessDeleteForm(AccessForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'