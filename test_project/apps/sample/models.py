# -*- coding: utf-8 -*-

from django.db import models

from cms.models import CMSPlugin


class Sample(models.Model):

    name = models.CharField('name', max_length=20, blank=False, default='')
    message = models.TextField('message')

    def __str__(self):
        return self.name


class SamplePluginModel(CMSPlugin):

    def __str__(self):
        return "Sample plugin {0}".format(self.id)
