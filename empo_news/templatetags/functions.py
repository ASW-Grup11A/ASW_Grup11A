from django import template

register = template.Library()


@register.filter
def get_class(obj):
    return obj.get_type()
