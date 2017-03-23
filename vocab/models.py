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
        

@python_2_unicode_compatible
class Process(models.Model):
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
        
        
@python_2_unicode_compatible
class EconomicResource(models.Model):
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
        

@python_2_unicode_compatible
class Action(models.Model):
    name = models.CharField(_('name'), max_length=255)
    note = models.TextField(_('note'), blank=True, null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name       

@python_2_unicode_compatible
class QuantityKind(models.Model):
    # qudt:QuantityKind
    name = models.CharField(_('name'), max_length=255)
    
    
@python_2_unicode_compatible
class Unit(models.Model):
    # qudt:Unit
    quantity_kind = models.ForeignKey(QuantityKind,
        verbose_name=_('quantity kind'), related_name="units")
    name = models.CharField(_('name'), max_length=255)
    
          
@python_2_unicode_compatible
class QuantityValue(models.Model):
    # qudt:QuantityValue
    numeric_value = models.DecimalField(_('quantity'), max_digits=11, decimal_places=4) #todo: embiggen?
    unit = models.ForeignKey(Unit,
        verbose_name=_('unit'), related_name="quantity_values")
    
    
@python_2_unicode_compatible
class EconomicEvent(models.Model):
    action = models.ForeignKey(Action,
        verbose_name=_('action'), related_name="events")
    provider = models.ForeignKey(Agent,
        verbose_name=_('provider'), related_name="provided events")
    receiver = models.ForeignKey(Agent,
        verbose_name=_('receiver'), related_name="received events")
    resource = models.ForeignKey(EconomicResource,
        blank=True, null=True,
        verbose_name=_('resource'), related_name='events')
    process = models.ForeignKey(Process,
        blank=True, null=True,
        verbose_name=_('process'), related_name='events',
        on_delete=models.SET_NULL)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    quantity_value = models.ForeignKey(QuantityValue,
        verbose_name=_('quantity value'), related_name="events")
    date_and_time = models.DateTimeField()
    
    class Meta:
        ordering = ('-date_and_time',)

    def __str__(self):
        return self.name
        
        

        