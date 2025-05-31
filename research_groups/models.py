from django.db import models

class ResearchGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # The reverse OneToOneFields are defined in the Professor model (see professors/models.py)

    def __str__(self):
        return self.name