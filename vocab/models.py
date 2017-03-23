# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Agent(models.Model):
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
        
