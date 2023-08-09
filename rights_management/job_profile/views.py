from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rights_management.department.models import Department
from rights_management.job_profile.forms import Job_profileForm, Job_profileDeleteForm
from rights_management.job_profile.models import Job_profile

@login_required
def job_profile_add(request):
    #print(request.user.get_all_permissions())
    if not request.user.has_perm('job_profile.add_job_profile'):
        app='No can add Job_profile'
        context = {'app': app}
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    form = Job_profileForm(request.POST or None)
    if form.is_valid():
        try:
            job_profile=form.save()
        except Exception:
            app = 'No can add this Job profile. First add a department.'
            context = {'app': app}
            return render(request, template_name='access_rights/no_can_add.html', context=context)
        job_profile.owner=request.user.id
        job_profile.save()
        return redirect('job_profile_list')
    app='Job Profile'
    context = {'form': form, "app": app}
    return render(request, template_name='department/department_add.html', context=context)

class job_profile_list(LoginRequiredMixin, generic.ListView):
    template_name = 'department/department_list.html'
    model = Job_profile
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        #print(Department.objects.all().first().id)
        contex = super().get_context_data(*args, **kwargs)
        #print(self.request.user.get_all_permissions())
        if not (self.request.user.has_perm('job_profile.change_job_profile') or\
                self.request.user.has_perm('job_profile.view_job_profile') or\
                self.request.user.has_perm('job_profile.delete_job_profile')):
            app_no_access = 'No can list, edit, delete Job Profile'
            app = 'Job Profile'
            context = {'app': app, 'app_no_access': app_no_access}
            return context
        contex['search'] = self.request.GET.get('search', '')
        app = 'Job Profile'
        contex['app']=app
        for i in contex['object_list']:
            i.job_access_all=", ".join(([j.right_name for j in i.job_access.all()]))
        return contex


class job_profile_details(LoginRequiredMixin, generic.DetailView):
    model = Job_profile
    template_name = 'job_profile/job_profile_details.html'

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not (self.request.user.has_perm('job_profile.change_job_profile') or\
                self.request.user.has_perm('job_profile.view_job_profile') or\
                self.request.user.has_perm('job_profile.delete_job_profile')):
            app = 'No can list, edit, delete Job Profile'
            context = {'app': app}
            return context

        contex['object'].job_access_all = ", ".join(([j.right_name for j in contex['object'].job_access.all()]))
        app = 'Job Profile'
        contex['app'] = app
        #print(contex['object'].job_access_all)
        return contex


class job_profile_edit(LoginRequiredMixin,generic.UpdateView):
    model = Job_profile
    template_name = 'job_profile/job_profile_edit.html'
    fields = ['name', 'description', 'job_access', 'in_department']
    success_url = reverse_lazy('job_profile_list')

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not self.request.user.has_perm('job_profile.change_job_profile'):
            app = 'No can list, edit, delete Job Profile'
            context = {'app': app}
            return context
        job_profile = self.get_object()
        if  self.request.user.id != contex['object'].owner and not self.request.user.is_superuser:
            app = 'User no can edit this Job Profile'
            context = {'app': app}
            return context
        app_current = 'Job Profile'
        contex['app_current'] = app_current
        return contex
@login_required
def job_profile_delete(request,pk):
    if not request.user.has_perm('job_profile.delete_job_profile'):
        app='No can delete Job profile'
        context = {'app': app}
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    job_profile = Job_profile.objects.get(pk=pk)
    job_profile.job_access_all = ", ".join(([j.right_name for j in job_profile.job_access.all()]))
    if  request.user.id != job_profile.owner and not request.user.is_superuser:
        app = 'User no can delete this Job profile'
        context = {'app': app}
        return render(request, template_name='access_rights/no_can_add.html', context=context)
    if request.method == 'POST':
        job_profile.delete()
        return redirect('job_profile_list')
    #form = Job_profileDeleteForm(initial=job_profile.__dict__)
    app_current = 'Job Profile'
    context = {'name':job_profile.name, 'description':job_profile.description, 'job_access_all': job_profile.job_access_all,'in_department': job_profile.in_department, 'app_current':app_current}
    return render(request, template_name='job_profile/job_profile_delete.html', context=context)


