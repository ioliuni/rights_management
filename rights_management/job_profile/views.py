from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rights_management.job_profile.forms import Job_profileForm, Job_profileDeleteForm
from rights_management.job_profile.models import Job_profile


def job_profile_add(request):
    form = Job_profileForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('job_profile_list')
    app='Job Profile'
    context = {'form': form, "app": app}
    return render(request, template_name='department/department_add.html', context=context)

class job_profile_list(generic.ListView):
    template_name = 'department/department_list.html'
    model = Job_profile
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        contex['search'] = self.request.GET.get('search', '')
        app = 'Job Profile'
        contex['app']=app
        for i in contex['object_list']:
            i.job_access_all=", ".join(([j.right_name for j in i.job_access.all()]))
        return contex

class job_profile_details(generic.DetailView):
    model = Job_profile
    template_name = 'job_profile/job_profile_details.html'

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        contex['search'] = self.request.GET.get('search', '')
        app = 'Job Profile'
        contex['app'] = app
        print('print')
        for i in contex:
            print(i)
        print(contex['object'].__dict__)
        print(contex['job_profile'].__dict__)
        print(contex['view'])
        # for i in contex['object']:
        #     print(i)
        return contex


class job_profile_edit(generic.UpdateView):
    model = Job_profile
    template_name = 'department/department_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('department_list')

def job_profile_delete(request,pk):
    job_profile = Job_profile.objects.get(pk=pk)
    if request.method == 'POST':
        job_profile.delete()
        return redirect('department_list')
    form = Job_profileDeleteForm(initial=job_profile.__dict__)
    context = {'form': form}
    return render(request, template_name='department/department_delete.html', context=context)


# Create your views here.
