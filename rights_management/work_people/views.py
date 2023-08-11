from django import forms
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rights_management.access_rights.views import nav_bar_list
from rights_management.department.models import Department
from rights_management.job_profile.models import Job_profile
from rights_management.work_people.forms import Work_peopleForm
from rights_management.work_people.models import Work_people


@login_required
def work_people_add(request):
    #print(request.user.get_all_permissions())
    if not request.user.has_perm('work_people.add_work_people'):
        app='No can add Work_people'
        context = {'app': app}
        context['view_all'] = nav_bar_list(request.user)['view_all']
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    form = Work_peopleForm(request.POST or None)
    if form.is_valid():
        work_people=form.save()
        work_people.owner=request.user.id
        work_people.save()
        return redirect('work_people_list')
    app='Work_people'
    context = {'form': form, "app": app}
    context['view_all'] = nav_bar_list(request.user)['view_all']
    return render(request, template_name='department/department_add.html', context=context)

class work_people_list(LoginRequiredMixin, generic.ListView):
    template_name = 'work_people/work_people_list.html'
    model = Work_people
    ordering = ['first_name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(first_name__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        #print(Department.objects.all().first().id)
        contex = super().get_context_data(*args, **kwargs)
        #print(self.request.user.get_all_permissions())
        if not (self.request.user.has_perm('work_people.change_work_people') or\
                self.request.user.has_perm('work_people.view_work_people') or\
                self.request.user.has_perm('work_people.delete_work_people')):
            app_no_access = 'No can list, edit, delete Work people'
            app = 'Work people'
            context = {'app': app, 'app_no_access': app_no_access}
            context['view_all'] = nav_bar_list(self.request.user)['view_all']
            return context
        contex['search'] = self.request.GET.get('search', '')
        app = 'Work people'
        contex['app']=app
        for i in contex['object_list']:
            i.with_job_profile_all=", ".join(([j.name for j in i.with_job_profile.all()]))
        contex['view_all'] = nav_bar_list(self.request.user)['view_all']
        return contex

class work_people_details(LoginRequiredMixin, generic.DetailView):
    model = Work_people
    template_name = 'job_profile/job_profile_details.html'

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not (self.request.user.has_perm('work_people.change_work_people') or \
                self.request.user.has_perm('work_people.view_work_people') or \
                self.request.user.has_perm('work_people.delete_work_people')):
            app = 'No can list, edit, delete Work people'
            context = {'app': app}
            context['view_all'] = nav_bar_list(self.request.user)['view_all']
            return context

        contex['object'].with_job_profile_all = ", ".join(([j.name for j in contex['object'].with_job_profile.all()]))
        app = 'Work people'
        contex['app'] = app
        contex['view_all'] = nav_bar_list(self.request.user)['view_all']
        #print(contex['object'].job_access_all)
        return contex


class work_people_edit(LoginRequiredMixin,generic.UpdateView):
    model = Work_people
    template_name = 'job_profile/job_profile_edit.html'
    fields = [ 'first_name', 'last_name', 'email', 'in_department']
    success_url = reverse_lazy('work_people_list')

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not self.request.user.has_perm('work_people.change_work_people'):
            app = 'No can list, edit, delete Work people'
            context = {'app': app}
            context['view_all'] = nav_bar_list(self.request.user)['view_all']
            return context
        work_people = self.get_object()
        if  self.request.user.id != contex['object'].owner and not self.request.user.is_superuser:
            app = 'User no can edit this Work people'
            context = {'app': app}
            context['view_all'] = nav_bar_list(self.request.user)['view_all']
            return context
        app_current = 'Work people'
        contex['app_current'] = app_current
        contex['view_all'] = nav_bar_list(self.request.user)['view_all']
        return contex

    def form_valid(self, form):
        # Изчистваме with_job_profile при промяна на in_department
        if 'in_department' in form.changed_data:
            form.instance.with_job_profile.clear()
        return super().form_valid(form)


class work_people_edit_profile(LoginRequiredMixin,generic.UpdateView):
    model = Work_people
    template_name = 'job_profile/job_profile_edit.html'
    fields = [ 'first_name', 'last_name', 'email', 'in_department', 'with_job_profile']
    #fields = [ 'first_name', 'last_name', 'email', 'in_department']
    success_url = reverse_lazy('work_people_list')

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not self.request.user.has_perm('work_people.change_work_people'):
            app = 'No can list, edit, delete Work people'
            context = {'app': app}
            context['view_all'] = nav_bar_list(self.request.user)['view_all']
            return context
        work_people = self.get_object()
        if  self.request.user.id != contex['object'].owner and not self.request.user.is_superuser:
            app = 'User no can edit this Work people'
            context = {'app': app}
            context['view_all'] = nav_bar_list(self.request.user)['view_all']
            return context
        app_current = "Profile's Work people"
        contex['app_current'] = app_current
        contex['in_department']=work_people.in_department
        #contex['form'].fields['in_department'].widget.attrs['readonly'] = True
        #print(contex['in_department'])
        contex['view_all'] = nav_bar_list(self.request.user)['view_all']
        return contex

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        department = self.object.in_department
        if department:
            form.fields['with_job_profile'].queryset = Job_profile.objects.filter(in_department=department)
        #form.fields['in_department'].widget.attrs['readonly'] = True
        form.fields['in_department'].widget = forms.HiddenInput()

        return form
@login_required
def work_people_delete(request,pk):
    if not request.user.has_perm('work_people.delete_work_people'):
        app='No can delete Work people'
        context = {'app': app}
        context['view_all'] = nav_bar_list(request.user)['view_all']
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    try:
        work_people = Work_people.objects.get(pk=pk)
    except Exception:
        app = 'No can delete this Work people.'
        context = {'app': app}
        context['view_all'] = nav_bar_list(request.user)['view_all']
        return render(request, template_name='access_rights/no_can_add.html', context=context)

    work_people.with_job_profile_all = ", ".join(([j.name for j in work_people.with_job_profile.all()]))
    if  request.user.id != work_people.owner and not request.user.is_superuser:
        app = 'User no can delete this Work people.'
        context = {'app': app}
        context['view_all'] = nav_bar_list(request.user)['view_all']
        return render(request, template_name='access_rights/no_can_add.html', context=context)
    if request.method == 'POST':
        try:
            work_people.delete()
        except Exception:
            app = 'No can delete this Work people.'
            context = {'app': app}
            context['view_all'] = nav_bar_list(request.user)['view_all']
            return render(request, template_name='access_rights/no_can_add.html', context=context)

        return redirect('work_people_list')
    #form = Job_profileDeleteForm(initial=job_profile.__dict__)
    app_current = 'Work people'
    context = {'first_name':work_people.first_name, 'last_name':work_people.last_name, 'email': work_people.email,'with_job_profile_all': work_people.with_job_profile_all,'in_department': work_people.in_department,'app_current': app_current }
    context['view_all'] = nav_bar_list(request.user)['view_all']
    return render(request, template_name='job_profile/job_profile_delete.html', context=context)

