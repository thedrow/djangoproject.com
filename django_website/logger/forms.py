from haystack.forms import ModelSearchForm

class NonEmptyModelSearchForm(ModelSearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
