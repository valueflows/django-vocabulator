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
]
