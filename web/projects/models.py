from django.db import models
from django.conf import settings

from profiles.models import Skill


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    requirements = models.TextField(default='')
    timeline = models.CharField(max_length=255, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='projects', null=True)

    @property
    def open_positions(self):
        return self.positions.exclude(applications__is_accepted=True)

    def __str__(self):
        return '{}'.format(self.title)


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, related_name='positions')
    skills = models.ManyToManyField(Skill, related_name='related_skills')

    def __str__(self):
        return '{}'.format(self.name)
