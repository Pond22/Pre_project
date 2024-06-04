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


@register.simple_tag(takes_context=True)
def reset_counter(context, counter_name):
    context[counter_name] = 0
    return ''

@register.simple_tag(takes_context=True)
def increment_counter(context, counter_name):
    if counter_name not in context:
        context[counter_name] = 0
    context[counter_name] += 1
    return context[counter_name]

@register.simple_tag(takes_context=True)
def get_sub_counter(context, main_counter_name, sub_counter_name):
    main_counter = context.get(main_counter_name, 0)
    if sub_counter_name not in context:
        context[sub_counter_name] = {}
    if str(main_counter) not in context[sub_counter_name]:
        context[sub_counter_name][str(main_counter)] = 0
    context[sub_counter_name][str(main_counter)] += 1
    return f"{main_counter}.{context[sub_counter_name][str(main_counter)]}"