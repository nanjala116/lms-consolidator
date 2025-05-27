from django.db import models

class Professor(models.Model):
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    # One-to-one relationship with research group (main_professor)
    research_group = models.OneToOneField(
        'research_groups.ResearchGroup',  # string reference to avoid import cycle
        related_name='main_professor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # One-to-one relationship where professor is the lead of a group
    leads_research_group = models.OneToOneField(
        'research_groups.ResearchGroup',  # string reference to avoid import cycle
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lead_professor'
    )
    bio = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} {self.name}"