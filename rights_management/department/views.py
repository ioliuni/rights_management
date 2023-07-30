from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rights_management.department.forms import DepartmentForm, DepartmentDeleteForm
from rights_management.department.models import Department

def department_add(request):
    if not request.user.has_perm('access_rights.add_department'):
        app='No can add Department'
        context = {'app': app}
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        department=form.save()
        department.user.set([request.user.id,])
        department.save()
        return redirect('department_list')
    app="Department"
    context = {'form': form, 'app':app}
    return render(request, template_name='department/department_add.html', context=context)

class department_list(generic.ListView):
    template_name = 'department/department_list.html'
    model = Department
    paginate_by = 3

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


class department_edit(generic.UpdateView):
    model = Department
    template_name = 'department/department_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('department_list')


def department_delete(request,pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    form = DepartmentDeleteForm(initial=department.__dict__)
    context = {'form': form}
    return render(request, template_name='department/department_delete.html', context=context)
