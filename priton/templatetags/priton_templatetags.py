from django import template

register = template.Library()

@register.filter(name="is_new_str")
def is_new_str(digit):
    if digit in [i*3 for i in range(1,15)]:
        return True
    else:
        return False