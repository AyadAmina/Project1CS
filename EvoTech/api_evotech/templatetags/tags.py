from django import template
from django.utils.translation import get_language
from django.utils.translation import activate, override


register = template.Library()


@register.simple_tag
def language_switcher(language_code):
    current_language = get_language()
    with override(language_code):
        language_url = '/contact.html'
        if language_code != current_language:
            language_url = f'/{language_code}/contact.html'
        return language_url