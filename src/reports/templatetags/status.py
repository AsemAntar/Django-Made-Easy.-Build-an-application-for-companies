from django import template


register = template.Library()


@register.filter(name="status")
def status(value, value2):
    try:
        if value - value2 >= 0:
            return "OK"
        else:
            return "Not Ok"
    except:
        pass
