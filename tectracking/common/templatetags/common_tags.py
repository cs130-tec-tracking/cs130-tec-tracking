from django import template
from django.contrib.auth.models import User

def in_group(user, groups):
    group_list = groups.split(',')

    if isinstance(user, User):
        user_groups = user.groups.values_list('name', flat=True)
        for group in group_list:
            if group in user_groups:
                return True

    return False

register = template.Library()
register.filter('in_group', in_group)
