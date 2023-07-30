from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rights_management.access_rights.forms import AccessForm, AccessDeleteForm
from rights_management.access_rights.models import Access_rights
# def can_add_access_rights(user):
#
#     return user.groups.filter(name='Can add access rights').exists()
def index(request):
    return render(request, template_name='access_rights/index.html')

@login_required
def access_rights_add(request):
    if not request.user.has_perm('access_rights.add_access_rights'):
        app='No can add Access_rights'
        context = {'app': app}
        return render(request,template_name='access_rights/no_can_add.html',context=context)
    form = AccessForm(request.POST or None)
    if form.is_valid():
        access_rights=form.save()
        # print(access_rights.__dict__)
        # print(request.user.id)
        access_rights.user.set([request.user.id,])
        access_rights.save()
        #form.save_m2m()
        return redirect('access_rights_list')
    context = {'form': form}
    return render(request,template_name='access_rights/access_rights_add.html',context=context)

class access_rights_list(LoginRequiredMixin, generic.ListView):

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
        return contex


class access_rights_details(LoginRequiredMixin, generic.DetailView):
    model = Access_rights
    template_name = 'access_rights/access_rights_details.html'


    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not (self.request.user.has_perm('access_rights.change_access_rights') or\
                self.request.user.has_perm('access_rights.view_access_rights') or\
                self.request.user.has_perm('access_rights.delete_access_rights')):
            app = 'No can list, edit, delete Access_rights'
            context = {'app': app}
            return context
        return contex


class access_rights_edit(LoginRequiredMixin, generic.UpdateView):
    model = Access_rights
    template_name = 'access_rights/access_rights_edit.html'
    fields = ['right_name', 'description', 'software']
    success_url = reverse_lazy('access_rights_list')

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(*args, **kwargs)
        if not self.request.user.has_perm('access_rights.change_access_rights'):
            app = 'No can edit Access_rights'
            context = {'app': app}
            return context
        access_rights = self.get_object()
        # for i in access_rights.user.all():
        #     print(i.id)
        #print(access_rights.user.all())
        if  self.request.user not in access_rights.user.all():
            app = 'User no can edit this Access_rights'
            context = {'app': app}
            return context

        #print(contex['object'].rightsuser.all())
        #RightsUser
        #print(contex['object'].__dict__)

        return contex

def access_rights_delete(request,pk):
    if not request.user.has_perm('access_rights.delete_access_rights'):
        app = 'No can delete Access_rights'
        context = {'app': app}
        return render(request, template_name='access_rights/no_can_add.html', context=context)
    access_rights = Access_rights.objects.get(pk=pk)
    access_rights_user = access_rights.user.all()
    if request.user not in access_rights_user:
        # print(request.user.id)
        # for i in access_rights_user:
        #     print(i.id)
        app = 'User no can delete this Access_rights'
        context = {'app': app}
        return render(request, template_name='access_rights/no_can_add.html', context=context)
    if request.method == 'POST':
        access_rights.delete()
        return redirect('access_rights_list')
    form = AccessDeleteForm(initial=access_rights.__dict__)
    context = {'form': form}
    return render(request, template_name='access_rights/access_rights_delete.html', context=context)
