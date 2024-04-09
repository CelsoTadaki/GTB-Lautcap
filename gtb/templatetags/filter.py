from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def titleToSlug(title):
    return slugify(title)

@register.filter
def toString(text):
    return str(text)
