from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[int(position)]
    except Exception:
        return ''

@register.filter
def char_at(value, position):
    try:
        return str(value)[int(position)]
    except Exception:
        return ''
