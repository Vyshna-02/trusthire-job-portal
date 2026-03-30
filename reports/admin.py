from django.contrib import admin
from .models import ScamReport

@admin.register(ScamReport)
class ScamReportAdmin(admin.ModelAdmin):
    list_display = ('job', 'reason', 'reported_by', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'reason', 'created_at')
    search_fields = ('job__title', 'reported_by__username', 'description')
    list_editable = ('is_resolved',) # Change status directly from the list view

    
   

