from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import ScamReport

@login_required
def report_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        ScamReport.objects.create(
            job=job,
            reported_by=request.user,
            reason=reason
        )

        messages.success(request, "Report submitted. Admin will review.")
        return redirect('job_list')

    return render(request, 'reports/report_job.html', {'job': job})
