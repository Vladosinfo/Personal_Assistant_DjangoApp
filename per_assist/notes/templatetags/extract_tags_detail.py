from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def format_tags(tag_queryset):
    formatted_tags = ["<b>{}</b>".format(tag.name) for tag in tag_queryset]
    return format_html(" | ".join(formatted_tags))
    # return " | ".join([tag.name for tag in tag_queryset])