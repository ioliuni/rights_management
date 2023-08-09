from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rights_management import access_rights
from rights_management.access_rights.models import Access_rights
from rights_management.department.forms import DepartmentForm, DepartmentDeleteForm
from rights_management.department.models import Department
from rights_management.job_profile.models import Job_profile
from rights_management.work_people.models import Work_people


@login_required
def department_add(request):
    #print(request.user.get_all_permissions())
    if not request.user.has_perm('department.add_department'):
        app='No can add Department'
        context = {'app': app}
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        department=form.save()
        department.owner=request.user.id
        department.save()
        return redirect('department_list')
    app="Department"
    context = {'form': form, 'app':app}
    return render(request, template_name='department/department_add.html', context=context)

class department_list(generic.ListView):
    template_name = 'department/department_list.html'
    model = Department
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        contex['search'] = self.request.GET.get('search', '')
        app = "Department"
        contex['app'] = app
        return contex

class department_details(generic.DetailView):
    model = Department
    template_name = 'department/department_details.html'


class department_edit(LoginRequiredMixin, generic.UpdateView):
    model = Department
    template_name = 'department/department_edit.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('department_list')

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not self.request.user.has_perm('department.change_department'):
            app = 'No can edit Department'
            context = {'app': app}
            return context
        access_rights = self.get_object()
        # for i in access_rights.user.all():
        #     print(i.id)
        #print(access_rights.user.all())
        #print(self.request.user.id, contex['object'].owner)
        if  self.request.user.id != contex['object'].owner and not self.request.user.is_superuser:
            app = 'User no can edit this Department'
            context = {'app': app}
            return context
        return contex

@login_required
def department_delete(request,pk):
    if not request.user.has_perm('department.delete_department'):
        app = 'No can delete Department'
        context = {'app': app}
        return render(request, template_name='access_rights/no_can_add.html', context=context)
    department = Department.objects.get(pk=pk)
    if  request.user.id != department.owner and not request.user.is_superuser:
        app = 'User no can delete this Department'
        context = {'app': app}
        return render(request, template_name='access_rights/no_can_add.html', context=context)
    if request.method == 'POST':
        try:
            department.delete()
        except Exception:
            app = 'No can delete this Department. The Department is used.'
            context = {'app': app}
            return render(request, template_name='access_rights/no_can_add.html', context=context)
    
        return redirect('department_list')
    form = DepartmentDeleteForm(initial=department.__dict__)
    context = {'form': form}
    return render(request, template_name='department/department_delete.html', context=context)

class report(LoginRequiredMixin,generic.ListView):
    template_name = 'department/report.html'
    model = Department
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        contex['search'] = self.request.GET.get('search', '')
        app = "Department"
        contex['app'] = app
        return contex

class people_in_department(LoginRequiredMixin, generic.ListView):
    template_name = 'work_people/work_people_list.html'
    model = Work_people
    ordering = ['first_name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.department = get_object_or_404(Department, pk=self.kwargs["pk"])
        queryset= Work_people.objects.filter(in_department=self.department)
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
            return context
        contex['search'] = self.request.GET.get('search', '')
        app = 'Work people in Department'
        contex['app']=app

        for i in contex['object_list']:
            i.with_job_profile_all=", ".join(([j.name for j in i.with_job_profile.all()]))
            i.job_access_all = ""
            for k in i.with_job_profile.all():
                #print(k.__dict__)
                #print(k.job_access.all())
                i.job_access_all += "("+k.name+"): "
                i.job_access_all += ", ".join(([l.right_name for l in k.job_access.all()]))
                i.job_access_all+=" "

            #i.job_access_all = ", ".join(([j.right_name for j in i.with_job_profile.job_profile_set.all()]))
        return contex

class profile_in_department(LoginRequiredMixin, generic.ListView):
    template_name = 'department/department_list.html'
    model = Job_profile
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.department = get_object_or_404(Department, pk=self.kwargs["pk"])
        queryset = Job_profile.objects.filter(in_department=self.department)
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

class access_rights_in_profile (LoginRequiredMixin, generic.ListView):

    template_name = 'access_rights/access_rights_list.html'
    # queryset=Smetka_acc.objects.filter(smetka_num__gt=104)
    model = Access_rights
    ordering = ['right_name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(software__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        #print(self.request.user.has_perm('access_rights.add_access_rights','access_rights.add_access_rights','access_rights.add_access_rights', ))
        if not (self.request.user.has_perm('access_rights.change_access_rights') or\
                self.request.user.has_perm('access_rights.view_access_rights') or\
                self.request.user.has_perm('access_rights.delete_access_rights')):
            app = 'No can list, edit, delete Access_rights'
            context = {'app': app}
            return context
        contex['search'] = self.request.GET.get('search', '')
        contex[ 'app_current']="Access rights in profile"
        for i in contex['object_list']:
            #print(i.job_profile_set.all())
            i.profile_all = ", ".join(([j.name for j in i.job_profile_set.all()]))
            #print(i.profile_all)
            i.work_people_all=""
            for k in i.job_profile_set.all():
                # print(k.__dict__)
                # print(k.work_people_set.all()[0])
                i.work_people_all += "("+k.name+"): "
                i.work_people_all += ", ".join(([l.first_name+ " "+l.last_name for l in k.work_people_set.all()]))
                i.work_people_all+=" "
                #print(i.work_people_all)
        return contex
