from functools import reduce
from operator import or_

from django.apps import apps
from django.db.models import Q


class SearchMixin:
    search_keyword_arg = 'search_word'
    search_settings = {}
    lookup_expr = 'icontains'

    def get_search_word(self):
        return self.request.GET.get(self.search_keyword_arg)

    def build_search_query(self, fields, search_word):
        return reduce(or_, [Q(**{f'{field}__{self.lookup_expr}': search_word}) for field in fields])

    def get_search_results(self):
        search_word = self.get_search_word()
        results = {}
        if search_word == '':
            return results
        for model, fields in self.search_settings.items():
            app_name, model_name = model.split('.')
            ModelClass = apps.get_model(app_label=app_name, model_name=model_name)
            queryset = ModelClass.objects.filter(self.build_search_query(fields, search_word)).distinct()
            if not queryset.exists():
                continue
            results[model_name.lower()] = queryset
        return results
