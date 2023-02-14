from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html

from .models import Author, Book, Publisher, Store


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'written_books',)
    ordering = ['id']
    list_filter = ['age', ]
    search_fields = ('id', 'name', 'age',)
    actions_on_top = False
    actions_on_bottom = True
    list_display_links = ('id', 'name', 'age',)
    list_per_page = 10
    save_as = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        all_query = Book.objects.all()
        written = Prefetch('book_set', all_query, to_attr='written')
        return qs.prefetch_related(written)

    def written_books(self, obj):
        result = len(obj.written)
        return format_html("<b><i>{}</i></b>", result)
    written_books.short_description = "Written Books"


class BookInline(admin.StackedInline):
    model = Book
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("publisher").prefetch_related("authors").all()


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'published_total',)
    ordering = ['id']
    list_display_links = ('id', 'name',)
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True
    save_as = True
    search_fields = ('id', 'name',)

    inlines = [BookInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        all_query_1 = Book.objects.all()
        all_query_2 = Author.objects.all()
        published_1 = Prefetch('book_set', all_query_1, to_attr='published_1')
        published_2 = Prefetch('book_set__authors', all_query_2, to_attr='published_2')
        return qs.prefetch_related(published_1, published_2).all()

    def published_total(self, obj):
        result = len(obj.published_1)
        return format_html("<b><i>{}</i></b>", result)
    published_total.short_description = "Published Books"


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selling_total',)
    ordering = ['id']

    list_display_links = ('id', 'name',)
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True
    save_as = True
    filter_horizontal = ('books',)
    search_fields = ('id', 'name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        all_query = Book.objects.all()
        selling = Prefetch('books', all_query, to_attr='selling')
        return qs.prefetch_related(selling)

    def selling_total(self, obj):
        result = len(obj.selling)
        return format_html("<b><i>{}</i></b>", result)
    selling_total.short_description = "Selling Books"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Так вместо 9-ти, получается 10-ть запросов.
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related('publisher').prefetch_related("authors").all()
    #
    list_display = ['id', 'name', 'pages', 'price', 'rating', "publisher", "pubdate"]
    list_display_links = ('id', 'name', 'pages', 'price', 'rating', 'publisher', 'pubdate')
    ordering = ['id']
    list_filter = ('rating', "publisher", "pubdate")
    search_fields = ('id', 'name', 'pages', 'price', 'rating', "publisher", "pubdate")
    # fields = [('name', "pages",), ('price', 'rating',), 'publisher', 'pubdate']
    date_hierarchy = 'pubdate'
    actions_on_top = False
    actions_on_bottom = True
    actions_selection_counter = True  # By default
    empty_value_display = '-empty-'
    save_as = True
    list_per_page = 10
    filter_horizontal = ('authors',)
