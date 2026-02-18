from django.contrib import admin
from .models import ScamReport

@admin.register(ScamReport)
class ScamReportAdmin(admin.ModelAdmin):
    list_display = ('job', 'reported_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job__title', 'reported_by__username')

    
   

