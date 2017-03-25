# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(Agent)
admin.site.register(AgentRelationshipRole)
admin.site.register(AgentRelationship)

admin.site.register(Process)
admin.site.register(EconomicResource)

admin.site.register(Action)
admin.site.register(QuantityKind)
admin.site.register(Unit)
admin.site.register(QuantityValue)
admin.site.register(EconomicEvent)

