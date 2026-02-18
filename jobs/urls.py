from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('applications/<int:job_id>/', views.employer_applications, name='employer_applications'),
    path('applications/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('detail/<int:job_id>/', views.job_detail, name='job_detail'),

]



