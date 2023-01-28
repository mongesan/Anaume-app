from django import template

register = template.Library()


def to_comma(value):
    return value.replace("/", ",")
