from django.contrib import admin

from rights_management.access_rights.models import Access_rights


@admin.register(Access_rights)
class Access_rightsAdmin(admin.ModelAdmin):
    list_display = ['right_name', 'software' ]
    list_filter = ['software']
    search_fields = ['right_name']
    fields = [('right_name', 'software'), 'description']
    ordering = ['software']
