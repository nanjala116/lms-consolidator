from django.db import models
from professors.models import Professor

class Course(models.Model):
    code = models.CharField(max_length=100, unique=True)  # e.g., course-v1:GermanUDS+PRP_webbasics+2024_1
    name = models.CharField(max_length=200)  # Course title
    description = models.TextField(default='No description yet')
    start_date = models.DateField()
    format = models.CharField(max_length=50, default='Self-paced')

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name