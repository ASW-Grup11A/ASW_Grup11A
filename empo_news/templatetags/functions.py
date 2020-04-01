from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter
def get_class(contribution):
    return contribution.get_type()


@register.filter
def get_total_likes(contribution):
    return contribution.total_likes()


@register.filter
def is_liked(contribution):
    return contribution.is_liked()

# {% if request.user.is_authenticated %} per tenir un unic main
