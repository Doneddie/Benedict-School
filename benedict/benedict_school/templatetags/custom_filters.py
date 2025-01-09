from django import template

register = template.Library()

@register.filter
def get_first_age(value):
    """
    Returns the first age from a comma-separated string of ages
    """
    if value and isinstance(value, str):
        return value.split(',')[0]
    return value