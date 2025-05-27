from django.db import models

# Create your models here.
from django.db import models
from professors.models import Professor

class ResearchGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    lead = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
