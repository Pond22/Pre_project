from django import template
from django.utils.encoding import force_str 

register = template.Library()

@register.filter
def in_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    if user is None:
        return False
    group_list = force_str(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))