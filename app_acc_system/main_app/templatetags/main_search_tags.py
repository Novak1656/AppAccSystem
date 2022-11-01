import re

from django.db.models import QuerySet
from django.template import Library

register = Library()


@register.inclusion_tag('search/clients_section_search_results.html')
def get_clients_section_search_results(search_results: QuerySet, search_word: str) -> dict:
    return {'clients_search_results': search_results, 'search_word': search_word}


@register.inclusion_tag('search/contact_persons_section_search_results.html')
def get_contact_persons_section_search_results(search_results: QuerySet, search_word: str) -> dict:
    return {'contact_persons_search_results': search_results, 'search_word': search_word}


@register.inclusion_tag('search/contracts_section_search_results.html')
def get_contracts_section_search_results(search_results: QuerySet, search_word: str) -> dict:
    return {'contracts_search_results': search_results, 'search_word': search_word}


@register.inclusion_tag('search/equipments_section_search_results.html')
def get_equipments_section_search_results(search_results: QuerySet, search_word: str) -> dict:
    return {'equipments_search_results': search_results, 'search_word': search_word}


@register.inclusion_tag('search/applications_section_search_results.html')
def get_applications_section_search_results(search_results: QuerySet, search_word: str) -> dict:
    return {'applications_search_results': search_results, 'search_word': search_word}


@register.simple_tag(name='highlight_search_words')
def highlight_search_words(text: str, search_word: str) -> dict:
    result = dict(is_search=False, text=text)
    if search_word.casefold() in text.casefold():
        new_text = re.sub(f'({search_word})', r'<font class="text-danger">\1</font>', text, flags=re.IGNORECASE)
        result.update({'is_search': True, 'text': new_text})
    return result
