from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import ScamReport

@login_required
def report_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Security Check: Prevent Employers from reporting their own listings
    if job.employer == request.user:
        messages.error(request, "You cannot report your own job listing.")
        return redirect('job_detail', job_id=job.id)

    # Security Check: Prevent duplicate reports from the same user
    already_reported = ScamReport.objects.filter(job=job, reported_by=request.user).exists()
    if already_reported:
        messages.warning(request, "You have already submitted a report for this job.")
        return redirect('job_list')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description') # Added description for more detail

        ScamReport.objects.create(
            job=job,
            reported_by=request.user,
            reason=reason,
            description=description
        )

        messages.success(request, "Thank you. Our moderation team has been notified and will review this listing.")
        return redirect('job_list')

    return render(request, 'reports/report_job.html', {'job': job})
