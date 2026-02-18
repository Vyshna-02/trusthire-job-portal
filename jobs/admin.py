from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'employer__username')
    actions = ['approve_jobs']

    def approve_jobs(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected jobs approved successfully")
    approve_jobs.short_description = "Approve selected jobs"


