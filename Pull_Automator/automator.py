import re
import logging
import pandas as pd
import json
from collections import Counter

with open("Pull_Automator/References/materials.json") as f:
    items=json.load(f)

with open("Pull_Automator/References/item_lookup.json") as f:
    item_lookup=json.load(f)

with open("Pull_Automator/References/item_alternates.json") as f:
    alternate=json.load(f)

class InsufficientPoints(Exception):
    pass

class UnassignedItem(Exception):
    pass

class PointsExhausted(Exception):
    pass

class Employee:
    def __init__(self,row):
        self.Name=row[0]
        self.mining=row[1]
        self.hunting=row[2]
        self.mercantile=row[3]
        self.black_market=row[4]

        self.pulls={
            'mining':[],
            'hunting':[],
            'mercantile':[],
            'black_market':[]
        }

    def verify_ability(self,pull):
        score=getattr(self,pull.category)

        if score<pull.cost:
            if score==0:
                raise PointsExhausted
            raise InsufficientPoints

        setattr(self,pull.category,score-pull.cost)
        self.pulls[pull.category].append(pull.item)

class Pull:
    def __init__(self,item):
        ref=item_lookup[item.lower()]
        self.item=item.lower()
        self.cost=ref['points']
        self.category=ref['cat']

class OrderManager:
    def __init__(self,orders):

        self.unrecognized_items=[]
        self.unassigned_items=[]

        self.parsed_order_list={
            'mining':[],
            'hunting':[],
            'mercantile':[],
            'black_market':[]
        }

        for item in orders:
            try:
                pull=Pull(item)
                self.parsed_order_list[pull.category].append(pull)
            except KeyError:
                self.unrecognized_items.append(item)

class AssignmentManager:
    def __init__(self,table,order_list):
        self.employees=[Employee(vals) for vals in table.values()]
        self.orders=OrderManager(order_list)

        self._assign_orders()
        self.assignments=self._build_dataframe()
        self.unassigned_items=self.count_items(self.orders.unassigned_items)
        self.unrecognized_items=self.count_items(self.orders.unrecognized_items)
    
    def count_items(self,items):
        return dict(Counter(items))


    def _assign_orders(self):

        for category,pulls in self.orders.parsed_order_list.items():

            for pull in pulls:

                assigned=False

                for emp in self.employees:
                    try:
                        emp.verify_ability(pull)
                        assigned=True
                        break
                    except (InsufficientPoints,PointsExhausted):
                        continue

                if not assigned:
                    self.orders.unassigned_items.append(pull.item)


    def _build_dataframe(self):

        rows=[]

        for e in self.employees:
            rows.append([
                e.Name,
                e.pulls['mining'],
                e.pulls['hunting'],
                e.pulls['mercantile'],
                e.pulls['black_market']
            ])

        return pd.DataFrame(
            rows,
            columns=['Employee','Mining','Hunting','Mercantile','Black_Market']
        )

def assign_pulls(employees,orders):
    ass=AssignmentManager(employees,orders)
    return ass