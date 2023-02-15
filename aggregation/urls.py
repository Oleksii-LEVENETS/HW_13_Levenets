from django.urls import path

from . import views


app_name = "aggregation"

urlpatterns = [
    path('', views.index, name='index'),

    path('author_list/', views.AuthorListView.as_view(), name='author-list'),
    path('publisher_list/', views.PublisherListView.as_view(), name='publisher-list'),
    path('book_list/', views.BookListView.as_view(), name='book-list'),
    path('store_list/', views.StoreListView.as_view(), name='store-list'),

    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher-detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store-detail'),

    path('reminder_form', views.reminder_form, name='reminder_form'),
]
