from django.db import models
from professors.models import Professor

class PhDStudent(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=10)  # e.g., Mr., Ms., Dr.
    supervisor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    research_topic = models.CharField(max_length=255)