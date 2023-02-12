from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.list import ListView

from aggregation.models import Author, Book, Publisher, Store


# Create your views here.
def index(request):
    return render(request, 'aggregation/index.html')

"""
path('authors_list/', AuthorsListView.as_view(), name='authors-list'),
    path('publishers_list/', PublishersListView.as_view(), name='publishers-list'),
    path('books_list/', BooksListView.as_view(), name='books-list'),
    path('stores_list/', StoresListView.as_view(), name='stores-list'),

    path('author/<int:id>/', AuthorDetailView.as_view(), name='author-detail'),
    path('publisher/<int:id>/', PublisherDetailView.as_view(), name='publisher-detail'),
    path('book/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('store/<int:id>/', StoreDetailView.as_view(), name='store-detail'),
"""


class AuthorListView(ListView):
    model = Author

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
