from django.db import models

# Create your models here.
from django.db import models
from professors.models import Professor

class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    instructor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
