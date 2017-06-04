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
from utils import *


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
    return "".join(["http://", Site.objects.get_current().domain])
    
def camelcase(name):
     return ''.join(x.capitalize() or ' ' for x in name.split(' '))
 
def camelcase_lower(name):
    pname = camelcase(name)
    return pname[0].lower() + pname[1:]
    
def get_lod_setup_items():
    
    path = get_url_starter() + "/vocab/"
    #instance_abbrv = Site.objects.get_current().domain.split(".")[0]
    instance_abbrv = "vocabulator"
    
    #import pdb; pdb.set_trace()
    context = {
        "vf": "https://w3id.org/valueflows/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "rdfs:label": { "@container": "@language" },
        "foaf": "http://xmlns.com/foaf/0.1/",
        "org": "http://www.w3.org/ns/org#",
        "Agent": "vf:Agent",
        "Person": "foaf:Person",
        "Organization": "org:Organization",
        "url":  { "@id": "vf:url", "@type": "@id" },
        "image": { "@id": "vf:image", "@type": "@id" },
        #"displayName": "vf:displayName",
        #"displayNameMap": { "@id": "displayName", "@container": "@language" },
        "Relationship": "vf:Relationship",
        "subject": { "@id": "vf:subject", "@type": "@id" },
        "object": { "@id": "vf:object", "@type": "@id" },
        "relationship": { "@id": "vf:relationship", "@type": "@id" },
        #"member": { "@id": "vf:member", "@type": "@id" }
        "Process": "vf:Process",
        "plannedStart": "xsd:String", #?
        "plannedDuration": "qudt:quantityValue", #?
        "isFinished": "xsd:boolean",
        "label": "skos:prefLabel",
        "labelMap": { "@id": "skos:prefLabel", "@container": "@language" },
        "note": "skos:note",
        "noteMap": { "@id": "skos:note", "@container": "@language" },
        "inverseOf": "owl:inverseOf",
        instance_abbrv: path,
    }
    
    store = Graph()
    store.bind("foaf", FOAF)
    store.bind("rdf", RDF)
    store.bind("rdfs", RDFS)
    store.bind("owl", OWL)
    store.bind("skos", SKOS)
    #org_ns = Namespace("http://www.w3.org/ns/org#")
    #store.bind("org", org_ns)
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
        ser = serializers.serialize(format, agents,
        use_natural_foreign_keys=True, use_natural_primary_keys=True,
        indent=4)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        for agent in agents:
            ref = URIRef(instance_abbrv + ":agent/" + str(agent.id) + "/")
            if agent.agent_subclass == "Person":
                store.add((ref, RDF.type, FOAF.Person))
            elif agent.agent_subclass == "Organization":
                org_ns = Namespace("http://www.w3.org/ns/org#")
                store.add((ref, RDF.type, org_ns.Organization)) 
            store.add((ref, vf_ns["label"], Literal(agent.name, lang="en")))
            #todo: image, url, primaryLocation, note; and also make sure we are using label instead of name
        ser = store.serialize(format=format, context=context, indent=4)
    #import pdb; pdb.set_trace()
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)

def agent(request, agent_id, format='json-ld'):
    #import pdb; pdb.set_trace()
    agent = Agent.objects.get(id=agent_id)
    agents = []
    agents.append(agent)
    if format == "json" or format == "yaml":
        ser = serializers.serialize(format, agents,
        use_natural_foreign_keys=True, use_natural_primary_keys=True,
        indent=4)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        ref = URIRef(instance_abbrv + ":agent/" + str(agent.id) + "/")
        if agent.agent_subclass == "Person":
            store.add((ref, RDF.type, FOAF.Person))
        elif agent.agent_subclass == "Organization":
            org_ns = Namespace("http://www.w3.org/ns/org#")
            store.add((ref, RDF.type, org_ns.Organization)) 
        store.add((ref, vf_ns["label"], Literal(agent.name, lang="en")))
        ser = store.serialize(format=format, context=context, indent=4)
    #import pdb; pdb.set_trace()
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)
    
def agentrelationships(request, format='json-ld'):
    associations = AgentRelationship.objects.all()
    #import pdb; pdb.set_trace()
    if format == "json" or format == "yaml":
        ser = serializers.serialize(format, associations,
            fields=('subject','relationship', 'object'),
            use_natural_foreign_keys=True, use_natural_primary_keys=True,
            indent=4)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        for a in associations:
            ref = URIRef(instance_abbrv + ":agent-relationship/" + str(a.id) + "/")
            inv_ref = URIRef(instance_abbrv + ":agent-relationship-inv/" + str(a.id) + "/")
            ref_subject = URIRef(instance_abbrv + ":agent/" + str(a.subject.id) + "/")
            ref_object = URIRef(instance_abbrv + ":agent/" + str(a.object.id) + "/")
            property_name = camelcase_lower(a.relationship.label)
            #inv_property_name = camelcase_lower(a.relationship.inverse_label)
            ref_relationship = URIRef(instance_abbrv + ":agent-relationship-role/" + property_name)
            #inv_ref_relationship = URIRef(instance_abbrv + ":agent-relationship-role/" + inv_property_name)
            #todo: change to store one and only one instance of relationship
            #and change Relationship to AgentRelationship
            store.add((ref, RDF.type, vf_ns["AgentRelationship"]))
            store.add((ref, vf_ns["subject"], ref_subject)) 
            store.add((ref, vf_ns["object"], ref_object))
            store.add((ref, vf_ns["relationship"], ref_relationship))
            
            #store.add((inv_ref, RDF.type, vf_ns["AgentRelationship"]))
            #store.add((inv_ref, vf_ns["object"], ref_subject)) 
            #store.add((inv_ref, vf_ns["subject"], ref_object))
            #store.add((inv_ref, vf_ns["relationship"], inv_ref_relationship))
            
        ser = store.serialize(format=format, context=context, indent=4)
    #import pdb; pdb.set_trace()
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)


def agent_relationships_as_subject(request, agent_id, format='json-ld'):
    #import pdb; pdb.set_trace()
    agent = Agent.objects.get(id=agent_id)
    associations = agent.subject_relationships.all()
    if format == "json" or format == "yaml":
        ser = serializers.serialize(format, associations,
            fields=('subject','relationship', 'object'),
            use_natural_foreign_keys=True, use_natural_primary_keys=True,
            indent=4)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        for a in associations:
            ref = URIRef(instance_abbrv + ":agent-relationship/" + str(a.id) + "/")
            inv_ref = URIRef(instance_abbrv + ":agent-relationship-inv/" + str(a.id) + "/")
            ref_subject = URIRef(instance_abbrv + ":agent/" + str(a.subject.id) + "/")
            ref_object = URIRef(instance_abbrv + ":agent/" + str(a.object.id) + "/")
            property_name = camelcase_lower(a.relationship.label)
            #inv_property_name = camelcase_lower(a.relationship.inverse_label)
            ref_relationship = URIRef(instance_abbrv + ":agent-relationship-role/" + property_name)
            #inv_ref_relationship = URIRef(instance_abbrv + ":agent-relationship-role/" + inv_property_name)
            #todo: change to store one and only one instance of relationship
            #and change Relationship to AgentRelationship
            store.add((ref, RDF.type, vf_ns["AgentRelationship"]))
            store.add((ref, vf_ns["subject"], ref_subject)) 
            store.add((ref, vf_ns["object"], ref_object))
            store.add((ref, vf_ns["relationship"], ref_relationship))
        ser = store.serialize(format=format, context=context, indent=4)
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)


def agents_subject_of(request, agent_id, format='json-ld'):
    #import pdb; pdb.set_trace()
    agent = Agent.objects.get(id=agent_id)
    associations = agent.subject_relationships.all()
    agents = []
    for assoc in associations:
        agents.append(assoc.object)
    if format == "json" or format == "yaml":
        ser = serializers.serialize(format, agents,
        use_natural_foreign_keys=True, use_natural_primary_keys=True,
        indent=4)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        for agent in agents:
            ref = URIRef(instance_abbrv + ":agent/" + str(agent.id) + "/")
            if agent.agent_subclass == "Person":
                store.add((ref, RDF.type, FOAF.Person))
            elif agent.agent_subclass == "Organization":
                org_ns = Namespace("http://www.w3.org/ns/org#")
                store.add((ref, RDF.type, org_ns.Organization)) 
            store.add((ref, vf_ns["label"], Literal(agent.name, lang="en")))
            #todo: image, url, primaryLocation, note; and also make sure we are using label instead of name
        ser = store.serialize(format=format, context=context, indent=4)
    #import pdb; pdb.set_trace()
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)

def processes(request, format='json-ld'):
    processes = Process.objects.all()
    if format == "json" or format == "yaml":
        ser = serializers.serialize(format, processes,
        use_natural_foreign_keys=True, use_natural_primary_keys=True,
        indent=4)
    else:
        path, instance_abbrv, context, store, vf_ns = get_lod_setup_items()
        for process in processes:
            ref = URIRef(instance_abbrv + ":process/" + str(process.id) + "/")
            store.add((ref, RDF.type, vf_ns["Process"]))            
            #name, plannedStart, plannedDuration, isFinished, note
            store.add((ref, vf_ns["label"], Literal(process.name, lang="en")))
            store.add((ref, vf_ns["plannedStart"], Literal(process.planned_start))) #todo:fix
            store.add((ref, vf_ns["plannedDuration"], Literal(process.planned_duration))) #todo:fix
            store.add((ref, vf_ns["isFinished"], Literal(process.is_finished))) #todo:fix
        ser = store.serialize(format=format, context=context, indent=4)
    #import pdb; pdb.set_trace()
    content_type = CONTENT_TYPES[format]
    return HttpResponse(ser, content_type=content_type)

def incoming(request):
    ends = end_resources()
    end = ends[0]
    flows = end.incoming_flows()
    for f in flows:
        f.sid = f.class_name() + str(f.id)
        if f.next:
            for n in f.next:
                f.parent = n.class_name() + str(n.id)
        else:
            f.parent = "#"
    return render(request, "vocab/incoming_flows.html", {
        "flows": flows,
    })
    
def process_flow(request):
    ends = end_resources()
    end = ends[0]
    nodes = [f for f in end.incoming_flows() if f.label()]
    nodes = list(set(nodes))
    #nodes = end.incoming_flows()
    edges = []
    #import pdb; pdb.set_trace()
    for f in nodes:
        f.sid = f.class_name() + str(f.id)
        for p in f.preds:
            if p.label():
                pred = p.class_name() + str(p.id)
                edges.append([pred, f.sid])
    roots = [n for n in nodes if not n.preds]
    roots = [r for r in roots if not r.class_name() == "EconomicEvent"]
    
    #import pdb; pdb.set_trace()    
    return render(request, "vocab/process_flow.html", {
        "nodes": nodes,
        "edges": edges,
        "roots": roots,
    })

