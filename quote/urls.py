from django.urls import path

from . import views


app_name = "quote"

urlpatterns = [
    path('', views.index, name='index'),

    path('author_list/', views.AuthorListView.as_view(), name='author-list'),
    path('quote_list/', views.QuoteListView.as_view(), name='quote-list'),

    path('author_detail/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('quote_detail/<int:pk>/', views.QuoteDetailView.as_view(), name='quote-detail'),
]
