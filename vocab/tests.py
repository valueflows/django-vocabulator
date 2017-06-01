# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import *

from django.utils import timezone
from django.test import TestCase
from models import *
from utils import *

# Create your tests here.

class ProcessNeighborsTest(TestCase):
    
        def setUp(self):
            component = EconomicResource.objects.create(name="Test Component")
            component_process = Process.objects.create(name="Create Component")
            product = EconomicResource.objects.create(name="Test Product")
            product_process = Process.objects.create(name="Create Product")
            count_kind = QuantityKind.objects.create(name="Count")
            each = Unit.objects.create(quantity_kind=count_kind, name="Each")
            one = QuantityValue.objects.create(
                numeric_value=Decimal("1.0"),
                unit=each)
            two = QuantityValue.objects.create(
                numeric_value=Decimal("2.0"),
                unit=each)
            now = timezone.now()
            alice = Agent.objects.create(name="alice")
            bob = Agent.objects.create(name="bob")
            carol = Agent.objects.create(name="carol")
            consume = Action.objects.create(label="Consume", resource_effect="decrement")
            produce = Action.objects.create(label="Produce", resource_effect="increment")
            
            create_component = EconomicEvent.objects.create(
                action=produce,
                provider=alice,
                receiver=bob,
                resource=component,
                process=component_process,
                quantity_value=two,
                date_and_time=now)
                
            consume_component = EconomicEvent.objects.create(
                action=consume,
                provider=bob,
                receiver=carol,
                resource=component,
                process=product_process,
                quantity_value=one,
                date_and_time=now)
                
            create_product = EconomicEvent.objects.create(
                action=produce,
                provider=carol,
                receiver=carol,
                resource=product,
                process=product_process,
                quantity_value=one,
                date_and_time=now)
                
        def test_process_neighbors(self):
            component_process = Process.objects.get(name="Create Component")
            product_process = Process.objects.get(name="Create Product")
            product_prevs = product_process.previous_processes()
            component_prevs = component_process.previous_processes()
            product_nexts = product_process.next_processes()
            component_nexts = component_process.next_processes()
            
            self.assertEqual(len(product_prevs), 1)
            self.assertIn(component_process, product_prevs)
            self.assertEqual(len(component_prevs), 0)
            self.assertEqual(len(component_nexts), 1)
            self.assertIn(product_process, component_nexts)
            self.assertEqual(len(product_nexts), 0)
            
        def test_incoming_flows(self):
            ends = end_resources()
            end = ends[0]
            flows = end.incoming_flows()
            self.assertEqual(len(flows), 7)
            roots = [f for f in flows if not f.next]
            self.assertEqual(len(roots), 1)
            root = roots[0]
            self.assertEqual(root, end)
            
            this = flows[len(flows)-1]
            next = this.next
            
            while next:
                next = this.next
                if next:
                    this = next
            self.assertEqual(root, this)
            
        def test_topological_sort(self):
            ends = end_resources()
            end = ends[0]
            topo = end.topological_sorted_inflows()
            component_process = Process.objects.get(name="Create Component")
            self.assertEqual(topo[0], component_process)
   

            