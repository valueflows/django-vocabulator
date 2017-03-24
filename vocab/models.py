# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


AGENT_SUBCLASS_OPTIONS = (
    ('person', _('Person')),
    ('organization', _('Organization')),
)


@python_2_unicode_compatible
class Agent(models.Model):
    """
    vf:Agent: 
    https://valueflows.gitbooks.io/valueflows/content/introduction/agents.html
    https://valueflows.gitbooks.io/valueflows/content/specification/generated-spec.html#d4e666
    """
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    agent_subclass =  models.CharField(_('subclass'),
        max_length=16, choices=AGENT_SUBCLASS_OPTIONS,
        default='person')
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

        
@python_2_unicode_compatible        
class AgentRelationshipRole(models.Model):
    """
    vf:AgentRelationshipRole:
    not yet defined
    """
    name = models.CharField(_('name'), max_length=255)
    inverse_name = models.CharField(_('name'), max_length=255)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
        
    
@python_2_unicode_compatible
class AgentRelationship(models.Model):
    """
    vf:Relationship:
    https://valueflows.gitbooks.io/valueflows/content/specification/generated-spec.html#d4e840    
    """
    subject = models.ForeignKey(Agent,
        verbose_name=_('subject', related_name="subject_relationships",))
    object = models.ForeignKey(Agent,
        verbose_name=_('object', related_name="object_relationships",))
    relationship = models.ForeignKey(AgentRelationshipRole,
        verbose_name=_('relationship', related_name="relationships",))
    context = models.ForeignKey(Agent,
        blank=True, null=True,
        verbose_name=_('context', related_name="context_relationships",))
        
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    

@python_2_unicode_compatible
class Process(models.Model):
    """
    vf:Process:
    https://valueflows.gitbooks.io/valueflows/content/introduction/processes.html
    https://valueflows.gitbooks.io/valueflows/content/specification/generated-spec.html#d4e829
    """
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    planned_start = models.DateTimeField(_('planned start'), blank=True, null=True)
    planned_duration = models.DurationField(_('planned duration'), blank=True, null=True)
    is_finished = models.BooleanField(_('is finished'), default=False)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
        
        
@python_2_unicode_compatible
class EconomicResource(models.Model):
    """
    vf.EconomicResource:
    https://valueflows.gitbooks.io/valueflows/content/introduction/resources.html
    https://valueflows.gitbooks.io/valueflows/content/specification/generated-spec.html#d4e758
    """
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), blank=True)
    note = models.TextField(_('note'), blank=True, null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

        
RESOURCE_EFFECT_OPTIONS = (
    ('increment', _('Increment')),
    ('decrement', _('Decrement')),
    ('none', _('None')),
)

@python_2_unicode_compatible
class Action(models.Model):
    """
    vf:Action:
    https://valueflows.gitbooks.io/valueflows/content/specification/generated-spec.html#d4e688
    """
    name = models.CharField(_('name'), max_length=255)
    note = models.TextField(_('note'), blank=True, null=True)
    resource_effect = models.CharField(_('resource effect'),
        max_length=16, choices=RESOURCE_EFFECT_OPTIONS)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name       

@python_2_unicode_compatible
class QuantityKind(models.Model):
    """
    qudt:QuantityKind:
    http://www.qudt.org/pages/QUDToverviewPage.html
    http://qudt.org/doc/2017/DOC_SCHEMA-QUDT-v2.0.html#Classes  
    """
    name = models.CharField(_('name'), max_length=255)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name 
    
    
@python_2_unicode_compatible
class Unit(models.Model):
    """
    qudt:Unit:
    http://qudt.org/doc/2017/DOC_VOCAB-UNITS-BASE.html
    http://qudt.org/doc/2017/DOC_SCHEMA-QUDT-v2.0.html#Classes
    """
    quantity_kind = models.ForeignKey(QuantityKind,
        verbose_name=_('quantity kind'), related_name="units")
    name = models.CharField(_('name'), max_length=255)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name 

        
@python_2_unicode_compatible
class QuantityValue(models.Model):
    """
    qudt:QuantityValue:
    http://qudt.org/doc/2017/DOC_SCHEMA-QUDT-v2.0.html#Classes
    """
    numeric_value = models.DecimalField(_('quantity'), max_digits=11, decimal_places=4) #todo: embiggen?
    unit = models.ForeignKey(Unit,
        verbose_name=_('unit'), related_name="quantity_values")
        
    class Meta:
        ordering = ('unit',)
        
    def __str__(self):
        return ' '.join([
            str(self.numeric_value),
            self.unit.name,
        ])
    
    
@python_2_unicode_compatible
class EconomicEvent(models.Model):
    """
    vf:EconomicEvent:
    https://valueflows.gitbooks.io/valueflows/content/specification/generated-spec.html#d4e747
    """
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
        
        return ' '.join([
            self.action.name,
            self.date_and_time.strftime('%Y-%m-%d'),
            'provider',
            self.provider.name,
            'receiver',
            self.receiver.name,
            self.quantity_value.__str__(),
            self.resource.__str__(),
        ])

        
        

        