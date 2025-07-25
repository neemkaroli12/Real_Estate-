from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """Replace substring from a string: {{ value|replace:"old,new" }}"""
    old, new = args.split(',')
    return value.replace(old, new)
