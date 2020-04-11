from django import template

register = template.Library()


@register.filter
def get_class(contribution):
    return contribution.get_type()


@register.filter
def is_liked(contribution):
    return contribution.is_liked()