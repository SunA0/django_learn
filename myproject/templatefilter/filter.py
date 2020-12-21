# 自定义标签
from django import template

register = template.Library()


@register.filter
def hello_my_filter(val):
    return val.replace('a', 'b')
