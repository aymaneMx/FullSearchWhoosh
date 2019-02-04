from django.shortcuts import render
from django.views.generic import TemplateView

from search.forms import searchForm
from search.whoosh import createSearchableData, findQuery


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request, **kwargs):
        createSearchableData()

        form = searchForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        global result
        form = searchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['query']
            result = findQuery(query, 3)
            print(result)

        context = {
            'form': form,
            'items': result,
        }
        return render(request, self.template_name, context)
