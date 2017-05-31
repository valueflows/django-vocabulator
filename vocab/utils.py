from models import *

def end_resources():
    ends = []
    candidates = EconomicEvent.objects.filter(action__resource_effect="increment")
    for event in candidates:
        if event.resource:
            if not event.resource.where_to():
                ends.append(event)
    return [end.resource for end in ends]