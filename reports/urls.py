from django.urls import path
from .views import report_job

urlpatterns = [
    path('job/<int:job_id>/', report_job, name='report_job'),
]
