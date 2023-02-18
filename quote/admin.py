from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html

from quote.models import Author, Quote


# Register your models here.
class QuoteInline(admin.StackedInline):
    model = Quote
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("author").all()


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'place_of_birth', 'written_quotes',)
    ordering = ['first_name']
    search_fields = ('id', 'last_name', 'first_name', 'date_of_birth', 'place_of_birth',)
    actions_on_top = False
    actions_on_bottom = True
    list_display_links = ('id', 'last_name', 'first_name', 'date_of_birth', 'place_of_birth',)
    list_per_page = 10
    save_as = True
    date_hierarchy = 'date_of_birth'

    inlines = [QuoteInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        all_query = Quote.objects.all()
        quotes = Prefetch('quote_set', all_query, to_attr='quotes')
        return qs.prefetch_related(quotes)

    def written_quotes(self, obj):
        result = len(obj.quotes)
        return format_html("<b><i>{}</i></b>", result)
    written_quotes.short_description = "Written Quotes"


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'text']
    list_display_links = ('id', 'title', 'author', 'text',)
    ordering = ['id']
    search_fields = ('id', 'title', 'author', 'text',)
    actions_on_top = False
    actions_on_bottom = True
    save_as = True
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("author").all()
