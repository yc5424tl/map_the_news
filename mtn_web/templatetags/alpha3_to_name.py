import pycountry
from django import template

register = template.Library()


@register.filter()
def alpha3_to_name(a3_code):
    return (pycountry.countries.get(alpha_3=a3_code.upper())).name
