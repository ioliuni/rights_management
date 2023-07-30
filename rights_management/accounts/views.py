from django import views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView

from rights_management.accounts.forms import RightsUserCreateForm, LoginForm
from rights_management.accounts.models import RightsUser




def user_register_add(request):
    form = RightsUserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    app='User'
    context = {'form': form, "app": app}
    return render(request, template_name='department/department_add.html', context=context)

class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login-page.html'
    next_page = reverse_lazy('department_list')

class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')

