from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    credits = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    format = models.CharField(max_length=50, blank=True)
    level = models.CharField(max_length=50, blank=True)
    professors = models.ManyToManyField(
        'professors.Professor',
        related_name='courses',
        through='relations.ProfessorCourse'
    )
    research_groups = models.ManyToManyField(
        'research_groups.ResearchGroup',
        related_name='courses',
        through='relations.CourseResearch'
    )

    def __str__(self):
        return self.name