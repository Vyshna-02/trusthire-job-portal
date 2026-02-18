from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication


# ===============================
# POST JOB (EMPLOYER ONLY)
# ===============================
@login_required
def post_job(request):
    user = request.user

    # Role check
    if user.role != 'EMPLOYER':
        messages.error(request, "Only employers can post jobs.")
        return redirect('home')

    # Employer verification check
    if not user.is_verified_employer:
        messages.error(request, "Your employer account is not verified yet.")
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')

        Job.objects.create(
            employer=user,
            title=title,
            description=description,
            location=location,
            is_approved=False  # Must be approved by admin
        )

        messages.success(request, "Job submitted for admin approval.")
        return redirect('home')

    return render(request, 'jobs/post_job.html')


# ===============================
# JOB LIST (ONLY APPROVED JOBS)
# ===============================
def job_list(request):
    jobs = Job.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ===============================
# JOB DETAIL (ONLY APPROVED JOBS)
# ===============================
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_approved=True)
    return render(request, 'jobs/job_detail.html', {'job': job})


# ===============================
# APPLY FOR JOB (JOB SEEKER ONLY)
# ===============================
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_approved=True)

    if request.user.role != 'JOBSEEKER':
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_list')

    # Prevent duplicate applications
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        JobApplication.objects.create(
            job=job,
            applicant=request.user
        )
        messages.success(request, "Application submitted successfully!")

    return redirect('job_list')


# ===============================
# EMPLOYER DASHBOARD
# ===============================
@login_required
def employer_dashboard(request):
    user = request.user

    if user.role != 'EMPLOYER':
        messages.error(request, "Only employers can access this page.")
        return redirect('home')

    jobs = Job.objects.filter(employer=user).order_by('-created_at')

    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})


# ===============================
# VIEW APPLICATIONS FOR A JOB (EMPLOYER)
# ===============================
@login_required
def employer_applications(request, job_id):
    user = request.user

    if user.role != 'EMPLOYER':
        messages.error(request, "Only employers can access this page.")
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, employer=user)

    applications = JobApplication.objects.filter(
        job=job
    ).order_by('-applied_at')

    return render(request, 'jobs/employer_applications.html', {
        'job': job,
        'applications': applications
    })


# ===============================
# JOB SEEKER DASHBOARD
# ===============================
@login_required
def jobseeker_dashboard(request):
    user = request.user

    if user.role != 'JOBSEEKER':
        messages.error(request, "Only job seekers can access this page.")
        return redirect('home')

    applications = JobApplication.objects.filter(
        applicant=user
    ).order_by('-applied_at')

    return render(request, 'jobs/jobseeker_dashboard.html', {
        'applications': applications
    })