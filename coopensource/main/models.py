from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.CharField(max_length=2048, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_url_on_catalog = models.URLField()
    project_url_external = models.URLField()
    project_description = models.TextField()
    keywords = models.CharField(max_length=500)
    fields_of_science = models.CharField(max_length=255)
    project_status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ])
    agency_sponsor = models.CharField(max_length=255)
    agency_sponsor_other = models.CharField(max_length=255, blank=True)
    geographic_scope = models.CharField(max_length=100)
    participant_age = models.CharField(max_length=255)
    project_goals = models.TextField(blank=True)
    participation_tasks = models.CharField(max_length=500)
    scistarter = models.BooleanField(default=True)
    email = models.EmailField()
    start_date = models.DateField()

    def __str__(self):
        return self.project_name
    