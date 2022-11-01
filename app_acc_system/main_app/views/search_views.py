from django.views.generic import TemplateView
from ..utils import SearchMixin


class SearchView(SearchMixin, TemplateView):
    template_name = 'search/search_results.html'
    search_settings = {
        'client_app.Clients': ['name', 'second_name', 'site', 'office_address', 'legal_address', 'note', 'inn', 'kpp', 'ogrn'],
        'client_app.ContactPersons': ['first_name', 'second_name', 'last_name', 'email', 'phone', 'note'],
        'client_app.Contracts': ['title', 'note'],
        'client_app.Equipments': ['name', 'note'],
        'main_app.Applications': ['subject', 'description', 'comments__comment_body']
    }

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['search_results'] = self.get_search_results()
        context['search_word'] = self.get_search_word()
        return context
