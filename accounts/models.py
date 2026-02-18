from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('JOB_SEEKER', 'Job Seeker'),
        ('EMPLOYER', 'Employer'),
        ('ADMIN', 'Admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='JOB_SEEKER'
    )
    is_verified_employer = models.BooleanField(default=False)


