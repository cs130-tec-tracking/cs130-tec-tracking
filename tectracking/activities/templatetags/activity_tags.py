from django.db.models.query import QuerySet
from tectracking.activities.models import Activity, Assignment
from django import template

def not_accepted(objects):
    if isinstance(objects, QuerySet):
        if objects.model is Activity:
            return objects.filter(status='N')
    return None

def accepted(objects):
    if isinstance(objects, QuerySet):
        if objects.model is Activity:
            return objects.filter(status='A')
        elif objects.model is Assignment:
            return objects.filter(activity__status='A')
    return None

def incomplete(objects):
    if isinstance(objects, QuerySet):
        if objects.model is Activity:
            return objects.filter(status='I')
        elif objects.model is Assignment:
            return objects.filter(activity__status='I')
    return None

def complete(objects):
    if isinstance(objects, QuerySet):
        if isinstance(objects.model, Activity):
            return objects.filter(status='C')
        elif isinstance(objects, Assignment):
            return objects.filter(activity__status='C')
    return None

register = template.Library()
register.filter('not_accepted', not_accepted)
register.filter('accepted', accepted)
register.filter('incomplete', incomplete)
register.filter('complete', complete)
