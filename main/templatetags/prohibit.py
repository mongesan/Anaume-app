from django import template

register = template.Library()
prohibition = ['.', '/', ',', '!', '?', '"', "'"]


@register.filter
def prohibit_exc(word):
    r = word
    if word[-1] in prohibition:
        r = word[:-1]
        if len(word) >= 2:
            if word[-2] in prohibition:
                r = word[:-2]
    return r


@register.filter
def prohibit(word):
    r = ""
    if word[-1] in prohibition:
        r = word[-1]
        if len(word) >= 2:
            if word[-2] in prohibition:
                r = word[-2:]
    return r
