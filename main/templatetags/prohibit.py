from django import template

register = template.Library()
prohibition = ['.', '/', ',', '!', '?', '"', "'"]


@register.filter
def prohibit_exc(word):
    r = word
    if word[0] in prohibition and len(word) > 2:
        word = word[1:]
        r = word
    if word[-1] in prohibition:
        r = word[:-1]
        if len(word) >= 2:
            if word[-2] in prohibition:
                r = word[:-2]
    return r


@register.filter
def prohibit_last(word):
    r = ""
    if word[-1] in prohibition:
        r = word[-1]
        if len(word) >= 2:
            if word[-2] in prohibition:
                r = word[-2:]
    return r


@register.filter
def prohibit_first(word):
    r = ""
    if word[0] in prohibition:
        r = word[0]
    return r