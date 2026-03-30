from django.db import models
from django.conf import settings
from jobs.models import Job

class ScamReport(models.Model):
    # Predefined reasons for easier admin filtering
    REASON_CHOICES = [
        ('scam', 'Fake Job / Scam'),
        ('money', 'Requesting Payment/Bank Details'),
        ('off_platform', 'Asking to communicate off-platform'),
        ('offensive', 'Inappropriate or Offensive Content'),
        ('other', 'Other / General Suspicion'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='scam_reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Use CharField with choices for the primary reason
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    
    # Use TextField for the user to explain the details
    description = models.TextField(blank=True, null=True)
    
    # Track status so admins can "resolve" reports
    is_resolved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Newest reports first
        # Ensures a user can't spam reports for the same job
        unique_together = ('job', 'reported_by')

    def __str__(self):
        return f"Report: {self.get_reason_display()} on {self.job.title}"


