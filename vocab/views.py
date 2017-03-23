# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.core import serializers

from rdflib import Graph, Literal, BNode
from rdflib.serializer import Serializer
from rdflib import Namespace, URIRef
from rdflib.namespace import FOAF, RDF, RDFS, OWL, SKOS
 
from urllib2 import urlopen
from io import StringIO

from models import *


CONTENT_TYPES = {
    'json-ld': 'application/json',
    "json": 'application/json',
    "yaml": 'text/x-yaml',
    'turtle': 'text/turtle',
    'n3': 'text/n3',
    'nt': 'application/n-triples',
    'xml': 'application/rdf+xml',
    #NQuads serialization only makes sense for context-aware stores
    #'nquads': 'application/n-quads',
}

        
def index(request):
    return HttpResponse("Hello, world. You're at the vocab index.")
    
def get_url_starter():
    return "".join(["https://", Site.objects.get_current().domain])
    
def camelcase(name):
     return ''.join(x.capitalize() or ' ' for x in name.split(' '))
 
def camelcase_lower(name):
    pname = camelcase(name)
    return pname[0].lower() + pname[1:]
    
def get_lod_setup_items():
    
    path = get_url_starter() + "/vocab/"
    instance_abbrv = Site.objects.get_current().domain.split(".")[0]
    
    context = {
        "vf": "https://w3id.org/valueflows/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        #"rdfs:label": { "@container": "@language" },
        "Agent": "vf:Agent",
        "Person": "vf:Person",
        "Group": "vf:Group",
        #"Organization": "vf:Organization",
        "url":  { "@id": "vf:url", "@type": "@id" },
        "image": { "@id": "vf:image", "@type": "@id" },
        #"displayName": "vf:displayName",
        #"displayNameMap": { "@id": "displayName", "@container": "@language" },
        "Relationship": "vf:Relationship",
        "subject": { "@id": "vf:subject", "@type": "@id" },
        "object": { "@id": "vf:object", "@type": "@id" },
        "relationship": { "@id": "vf:relationship", "@type": "@id" },
        #"member": { "@id": "vf:member", "@type": "@id" }
        "label": "skos:prefLabel",
        "labelMap": { "@id": "skos:prefLabel", "@container": "@language" },
        "note": "skos:note",
        "noteMap": { "@id": "skos:note", "@container": "@language" },
        "inverseOf": "owl:inverseOf",
        instance_abbrv: path,
    }
    
    store = Graph()
    #store.bind("foaf", FOAF)
    store.bind("rdf", RDF)
    store.bind("rdfs", RDFS)
    store.bind("owl", OWL)
    store.bind("skos", SKOS)
    #as_ns = Namespace("http://www.w3.org/ns/activitystreams#")
    #store.bind("as", as_ns)
    #schema_ns = Namespace("http://schema.org/")
    #store.bind("schema", schema_ns)
    #at_ns = Namespace(path + "agent-type/")
    #store.bind("at", at_ns)
    #aat_ns = Namespace(path + "agent-relationship-type/")
    #store.bind("aat", aat_ns)
    vf_ns = Namespace("https://w3id.org/valueflows/")
    store.bind("vf", vf_ns)
    instance_ns = Namespace(path)
    store.bind("instance", instance_ns)
    
    return path, instance_abbrv, context, store, vf_ns

def agents(request, format='json-ld'):
    agents = Agent.objects.all()
    if format == "json" or format == "yaml":
        ser = serializers.serialize(format, agents)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        for agent in agents:
            ref = URIRef(instance_abbrv + ":agent/" + str(agent.id) + "/")
            store.add((ref, RDF.type, vf_ns.Person))
            store.add((ref, vf_ns["label"], Literal(agent.name, lang="en")))            
        ser = store.serialize(format=format, context=context, indent=4)
    #import pdb; pdb.set_trace()
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)
    

        