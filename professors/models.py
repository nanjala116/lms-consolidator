from django.db import models

class Professor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=20)  # e.g., Dr., Prof.

    def __str__(self):
        return f"{self.title} {self.name}"