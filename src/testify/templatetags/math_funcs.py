from django import template

register = template.Library()


def negate(value):
    return -value


def mult(value, arg):
    return value * arg


@register.filter(name='div')
def div(value, arg):
    return value / arg


@register.simple_tag(name='expr')
def expr(value, *args):
    for idx, arg in enumerate(args, 1):
        value = value.replace(f'%{idx}', str(arg))
    return eval(value)


register.filter('negate', negate)
register.filter('mult', mult)
