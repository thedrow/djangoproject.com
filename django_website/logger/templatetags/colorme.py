from django import template

register = template.Library()


@register.filter
def colorize(value):
    if not value:
        return ""
    result = sum([ord(c) for c in value])
    return "#%X" % result
