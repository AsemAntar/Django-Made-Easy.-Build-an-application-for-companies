from django import template


register = template.Library()


@register.filter(name="subtract")
def subtract(val, val2):
    try:
        return val - val2
    except:
        pass
