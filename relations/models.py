from django.db import models

class ProfessorCourse(models.Model):
    professor = models.ForeignKey('professors.Professor', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('professor', 'course')

class CourseResearch(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    research_group = models.ForeignKey('research_groups.ResearchGroup', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'research_group')
        verbose_name = "Course research"
        verbose_name_plural = "Course researches"