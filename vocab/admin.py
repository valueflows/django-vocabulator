# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(AgentRelationshipRole)

admin.site.register(Process)
admin.site.register(EconomicResource)

admin.site.register(Action)
admin.site.register(QuantityKind)
admin.site.register(Unit)
admin.site.register(QuantityValue)
admin.site.register(EconomicEvent)

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'agent_subclass', 'url', 'note', 'created_by')
    list_filter = ['agent_subclass', 'created_by']
    search_fields = ['name',]


admin.site.register(Agent, AgentAdmin)


class AgentRelationshipAdmin(admin.ModelAdmin):
    list_display = ('subject', 'relationship', 'object', 'context', 'created_by')
    list_filter = ['relationship', 'created_by']


admin.site.register(AgentRelationship, AgentRelationshipAdmin)
