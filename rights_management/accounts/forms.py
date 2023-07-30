from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from rights_management.accounts.models import RightsUser


class RightsUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = RightsUser
        fields = ('username', 'email', )


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"}))
    password = forms.CharField(strip=False,
                               widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"}),)

class PetstagramUserEditForm(forms.ModelForm):
    class Meta:
        model= RightsUser
        fields=('username', 'first_name', 'last_name', 'email')
        exclude=('password',)
        labels={'username': 'Username', 'first_name':'First name' , 'last_name':  'Last name', 'email': 'Email' }
