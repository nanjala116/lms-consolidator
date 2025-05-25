from django.db import models

# Create your models here.
from django.db import models
from professors.models import Professor

class PhDStudent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    supervisor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
