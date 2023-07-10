from django import template

register = template.Library()

@register.filter
def custom_replace(value, arg):
    old, new = arg.split('/')
    return value.replace(arg, old, new)