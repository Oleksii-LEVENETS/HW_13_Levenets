from django.urls import path

from . import views
from .views import AuthorListView, AuthorDetailView

app_name = "aggregation"

urlpatterns = [
    path('', views.index, name='index'),

    path('author_list/', AuthorListView.as_view(), name='author-list'),
    # path('publisher_list/', PublisherListView.as_view(), name='publisher-list'),
    # path('book_list/', BookListView.as_view(), name='book-list'),
    # path('store_list/', StoreListView.as_view(), name='store-list'),
    #
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    # path('publisher/<int:id>/', PublisherDetailView.as_view(), name='publisher-detail'),
    # path('book/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    # path('store/<int:id>/', StoreDetailView.as_view(), name='store-detail'),
]
