# 自定义标签
from django import template

register = template.Library()


@register.simple_tag
def website_title_tag():
    return 'Joshua'
