from django.contrib import admin
from .models import MergeSession


@admin.register(MergeSession)
class MergeSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'primary_file_name', 'sheet_name', 'output_file_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['primary_file_name', 'output_file_name']
    readonly_fields = ['id', 'created_at', 'sheet_name', 'primary_file_name', 'all_files', 'selected_columns', 'output_file_name', 'status', 'error_message']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False