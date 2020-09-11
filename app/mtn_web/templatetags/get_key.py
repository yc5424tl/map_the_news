from django import template

register = template.Library()

# {{ foo_dict|get_key:foo_key }}


@register.filter
def get_key(dictionary, key):
    return dictionary.get(key)
