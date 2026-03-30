from django.urls import path
from . import views

urlpatterns = [
    # Main Job Browsing
    path('', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    
    # Employer Actions
    path('post/', views.post_job, name='post_job'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('applications/<int:job_id>/', views.employer_applications, name='employer_applications'),
    
    # Job Seeker Actions
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/seeker/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    
    # Support Actions
    path('report/<int:job_id>/', views.report_job, name='report_job'),
]



