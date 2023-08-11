from django.contrib import admin


from rights_management.access_rights.models import Access_rights, View_permission


@admin.register(Access_rights)
class Access_rightsAdmin(admin.ModelAdmin):
    list_display = ['right_name', 'software' ]
    list_filter = ['software']
    search_fields = ['right_name']
    fields = [('right_name', 'software'), 'description']
    ordering = ['software']
@admin.register(View_permission)
class View_permissionAdmin(admin.ModelAdmin):
    list_display = ['view_name', 'with_permission']