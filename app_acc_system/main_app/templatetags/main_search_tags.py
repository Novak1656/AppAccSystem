from django.template import Library

register = Library()


@register.inclusion_tag('search/clients_section_search_results.html')
def get_clients_section_search_results(search_results: object) -> dict:
    return {'clients_search_results': search_results}


@register.inclusion_tag('search/contact_persons_section_search_results.html')
def get_contact_persons_section_search_results(search_results: object) -> dict:
    return {'contact_persons_search_results': search_results}


@register.inclusion_tag('search/contracts_section_search_results.html')
def get_contracts_section_search_results(search_results: object) -> dict:
    return {'contracts_search_results': search_results}


@register.inclusion_tag('search/equipments_section_search_results.html')
def get_equipments_section_search_results(search_results: object) -> dict:
    return {'equipments_search_results': search_results}


@register.inclusion_tag('search/applications_section_search_results.html')
def get_applications_section_search_results(search_results: object) -> dict:
    return {'applications_search_results': search_results}
