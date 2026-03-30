from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication

# ===============================
# JOB LIST & DETAIL
# ===============================
def job_list(request):
    jobs = Job.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_approved=True)
    return render(request, 'jobs/job_detail.html', {'job': job})

# ===============================
# POST JOB (EMPLOYER ONLY)
# ===============================
@login_required
def post_job(request):
    if request.user.role != 'EMPLOYER':
        messages.error(request, "Only employers can post jobs.")
        return redirect('job_list')

    if not request.user.is_verified_employer:
        messages.error(request, "Your employer account is not verified yet.")
        return redirect('employer_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')

        Job.objects.create(
            employer=request.user,
            title=title,
            description=description,
            location=location,
            is_approved=False
        )
        messages.success(request, "Job submitted for admin approval.")
        return redirect('employer_dashboard')

    return render(request, 'jobs/post_job.html')

# ===============================
# APPLY FOR JOB (JOB SEEKER ONLY)
# ===============================
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_approved=True)

    if request.user.role != 'JOB_SEEKER':
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_list')

    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        JobApplication.objects.create(job=job, applicant=request.user)
        messages.success(request, "Application submitted successfully!")

    return redirect('jobseeker_dashboard')

# ===============================
# EMPLOYER VIEWS
# ===============================
@login_required
def employer_dashboard(request):
    if request.user.role != 'EMPLOYER':
        return redirect('home')
    
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})

@login_required
def employer_applications(request, job_id):
    if request.user.role != 'EMPLOYER':
        messages.error(request, "Access denied.")
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = JobApplication.objects.filter(job=job).order_by('-applied_at')

    return render(request, 'jobs/employer_applications.html', {
        'job': job,
        'applications': applications
    })

# ===============================
# JOB SEEKER VIEWS
# ===============================
@login_required
def jobseeker_dashboard(request):
    if request.user.role != 'JOB_SEEKER':
        return redirect('home')

    applications = JobApplication.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'jobs/jobseeker_dashboard.html', {'applications': applications})

# ===============================
# REPORT JOB
# ===============================
@login_required
def report_job(request, job_id):
    # Add your report logic here (or redirect to a report form)
    messages.info(request, f"Report received for job #{job_id}. Our team will review it.")
    return redirect('job_list')