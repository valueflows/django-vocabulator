from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"^agents/$", views.agents, name="agents"),
    url(r"^agents/(?P<format>[a-zA-Z0-9\-]+)/$", views.agents, name="agents_formatted"),
    url(r"^agentrelationships/$", views.agentrelationships, name="agent_relationships"),
    url(r"^agentrelationships/(?P<format>[a-zA-Z0-9\-]+)/$", views.agentrelationships, name="agent_relationships_formatted"),
    url(r"^agent/(?P<agent_id>\d+)/$", views.agent, name="agent"),
    url(r"^agent/(?P<agent_id>\d+)/(?P<format>[a-zA-Z0-9\-]+)/$", views.agent, name="agent_formatted"),
    url(r"^relationshipssubjectof/(?P<agent_id>\d+)/$", views.agent_relationships_as_subject, name="agent_relationships_as_subject"),
    url(r"^relationshipssubjectof/(?P<agent_id>\d+)/(?P<format>[a-zA-Z0-9\-]+)/$", views.agent_relationships_as_subject, name="agent_relationships_as_subject_formatted"),
    url(r"^agentssubjectof/(?P<agent_id>\d+)/$", views.agents_subject_of, name="agents_subject_of"),
    url(r"^agentssubjectof/(?P<agent_id>\d+)/(?P<format>[a-zA-Z0-9\-]+)/$", views.agents_subject_of, name="agents_subject_of_formatted"),
    url(r"^processess/$", views.processes, name="processes"),
    url(r"^processes/(?P<format>[a-zA-Z0-9\-]+)/$", views.processes, name="processes_formatted"),
    url(r"^incoming/$", views.incoming, name="incoming"),
    url(r"^process-flow/$", views.process_flow, name="process_flow"),
    url(r"^egg2worm-flow/$", views.egg2worm_flow, name="egg2worm_flow"),
    url(r"^process-resource-flow/$", views.process_resource_flow, name="process_resource_flow"),
    url(r"^processes-only/$", views.processes_only, name="processes_only"),
]
