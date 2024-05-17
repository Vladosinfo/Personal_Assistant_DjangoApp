from django import template

register = template.Library()


def tags(note_tags):
    string_list_tags = []
    for name in note_tags.all():
        string_list_tags.append(name)
    return string_list_tags

register.filter('tags', tags)
