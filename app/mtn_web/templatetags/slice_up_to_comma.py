from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def slice_up_to_comma(string_with_comma):
    index_of_first_comma = string_with_comma.find(',')
    if index_of_first_comma == -1:  # no comma in string
        return string_with_comma
    else:
        substring = string_with_comma[:index_of_first_comma]
        return substring
