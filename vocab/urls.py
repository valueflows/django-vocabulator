from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"^agents/$", views.agents, name="agent"),
    url(r"^agents/(?P<format>[a-zA-Z0-9\-]+)/$", views.agents, name="agent"),
    url(r"^agentrelationships/$", views.agentrelationships, name="agent"),
    url(r"^agentrelationships/(?P<format>[a-zA-Z0-9\-]+)/$", views.agentrelationships, name="agent"),
]
