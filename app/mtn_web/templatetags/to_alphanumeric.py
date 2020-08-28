from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter  # https://www.kite.com/python/answers/how-to-remove-all-non-alphanumeric-characters-from-a-string-in-python
@stringfilter
def to_alphanumeric(target_string: str):
    filter_alphanum = filter(str.isalnum, target_string)
    alphanum_string = "".join(filter_alphanum)
    return alphanum_string
