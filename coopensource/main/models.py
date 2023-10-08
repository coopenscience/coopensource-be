from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.CharField(max_length=2048, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Project(models.Model):
    project_id = models.CharField(1024, null=True, blank=True)
    project_name = models.TextField()
    project_url_on_catalog = models.URLField()
    project_url_external = models.URLField()
    project_description = models.TextField()
    keywords = models.TextField()
    fields_of_science = models.TextField()
    project_status = models.TextField()
    agency_sponsor = models.TextField()
    agency_sponsor_other = models.TextField()
    geographic_scope = models.TextField()
    participant_age = models.TextField()
    project_goals = models.CharField(null=True, blank=True)
    participation_tasks = models.TextField()
    scistarter = models.TextField()
    email = models.TextField()
    start_date = models.TextField()

    def __str__(self):
        return self.project_name
    