# 自定义标签
from django import template

register = template.Library()


@register.simple_tag
def add_str_tag(strs):
    return 'hello' % strs
