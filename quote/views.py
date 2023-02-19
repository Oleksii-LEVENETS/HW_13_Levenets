from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from quote.models import Author, Quote


# Create your views here.
def index(request):
    """View function for home page of Quote site."""
    # Generate counts of some of the main objects
    num_authors = Author.objects.count()
    num_quotes = Quote.objects.count()

    context = {
        'num_authors': num_authors,
        'num_quotes': num_quotes,
    }
    return render(request, 'quote/index.html', context=context)


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 20
    template_name = "quote/author_list.html"

    def get_queryset(self):
        return super().get_queryset().order_by('first_name')


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "quote/author_detail.html"

    # author_quotes
    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        author_quotes = Quote.objects.filter(author__id=self.object.id).annotate(num=Count("id"))
        context['author_quotes'] = author_quotes
        context['quotes_total'] = len(author_quotes)
        return context


class QuoteListView(generic.ListView):
    model = Quote
    template_name = "quote/quote_list.html"
    paginate_by = 10


class QuoteDetailView(generic.DetailView):
    model = Quote
    template_name = "quote/quote_detail.html"

    def get_context_data(self, **kwargs):
        context = super(QuoteDetailView, self).get_context_data(**kwargs)
        context['quote_author'] = Author.objects.get(id=self.object.author_id)
        return context
