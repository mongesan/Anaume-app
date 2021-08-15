from django import template
from django.shortcuts import get_object_or_404
from main.models import Fav

register = template.Library()


@register.simple_tag
def note_to_fav(user, note):
    if Fav.objects.filter(user=user, note=note).exists():
        return 'fas'
    else:
        return 'far'

