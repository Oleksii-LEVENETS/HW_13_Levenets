from aggregation.models import Author, Book, Publisher, Store

from django.db.models import Avg, Count
from django.shortcuts import render
from django.views import generic


# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_authors = Author.objects.count()
    num_publishers = Publisher.objects.count()
    num_books = Book.objects.count()
    num_stores = Store.objects.count()

    context = {
        'num_authors': num_authors,
        'num_publishers': num_publishers,
        'num_books': num_books,
        'num_stores': num_stores,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# List Views
class AuthorListView(generic.ListView):
    model = Author
    # paginate_by = 10
    queryset = Author.objects.annotate(num=Count("book__id"))
    context_object_name = "authors_books"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class PublisherListView(generic.ListView):
    model = Publisher
    # paginate_by = 10
    queryset = Publisher.objects.annotate(num=Count("book__id"))
    context_object_name = "publishers_books"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class BookListView(generic.ListView):
    model = Book
    paginate_by = 25
    queryset = Book.objects.select_related("publisher").order_by('name')


class StoreListView(generic.ListView):
    model = Store
    # paginate_by = 10
    queryset = Store.objects.annotate(num=Count("books__id"))
    context_object_name = "stores_books"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


# Detail Views
class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        book_author = Book.objects.filter(authors__id=self.object.id).annotate(num=Count("id"))
        context['author_books'] = book_author

        # Экономия одного запроса -- стоит ли len?
        context['written_total'] = len(book_author)
        # context['written_total'] = book_author.count()

        # Здесь prefetch_related("authors") экономии не дает, его можно убрать?
        context['author_avg_rating'] = round(Book.objects.prefetch_related("authors").filter(
                                authors=self.object.id).aggregate(a=Avg("rating"))["a"], 2)
        # context['author_avg_rating'] = round(Book.objects.filter(
        #     authors=self.object.id).aggregate(a=Avg("rating"))["a"], 2)
        return context


class PublisherDetailView(generic.DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super(PublisherDetailView, self).get_context_data(**kwargs)
        context['published_total'] = Book.objects.filter(publisher=self.object.id).count()
        context['publisher_books'] = Book.objects.filter(publisher=self.object.id)
        context['publisher_avg_rating'] = round(Book.objects.filter(
                                publisher=self.object.id).aggregate(a=Avg("rating"))["a"], 2)
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['available_stores'] = Store.objects.filter(books=self.object.id)
        context['books_authors'] = Author.objects.filter(book=self.object.id)

        return context


class StoreDetailView(generic.DetailView):
    model = Store
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        context['store_books'] = Book.objects.filter(store=self.object.id)
        context['selling_total'] = Book.objects.filter(store=self.object.id).count()
        return context
