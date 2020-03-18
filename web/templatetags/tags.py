from django import template
register = template.Library()

@register.simple_tag
def bgc(*args,**kwargs):
  return f'background-color: {args[0]}'