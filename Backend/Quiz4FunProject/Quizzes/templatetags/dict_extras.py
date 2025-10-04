from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acessar dict[key] no template"""
    if dictionary is None:
        return None
    return dictionary.get(key)
