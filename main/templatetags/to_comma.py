from django import template

register = template.Library()


@register.filter
def to_comma(value):
    return value.replace("/", ",")
