from django.db import models

class PhDStudent(models.Model):
    title = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=255)
    research_group = models.ForeignKey(
        'research_groups.ResearchGroup',  # Use string reference for cross-app relation
        on_delete=models.CASCADE,
        related_name='phd_students'
    )
    supervisor = models.ForeignKey(
        'professors.Professor',           # Use string reference for cross-app relation
        on_delete=models.CASCADE,
        related_name='phd_students'
    )
    enrollment_date = models.DateField()
    image_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "PhD student"
        verbose_name_plural = "PhD students"

    def __str__(self):
        return f"{self.title} {self.name}".strip()