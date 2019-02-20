from django import template

register = template.Library()


@register.filter(name='mlti')
def mlti(value1, value2):
    total = value1 * value2
    return total
