from django.contrib import admin
from django.db.models import Avg, Sum, SmallIntegerField
from django.utils.html import format_html

from .models import Author, Book, Publisher, Store


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'authors_books',)
    ordering = ['id']

    fieldsets = [
        ("Name", {"fields": ['name'], }),
        ("Age", {"fields": ["age"], }),
    ]

    list_filter = ['age', ]
    search_fields = ('id', 'name', 'age', )
    filter_horizontal = ('book',)

    def authors_books(self, obj):
        result = Book.objects.prefetch_related('authors').filter(authors__id=obj.id).count()
        return format_html("<b><i>{}</i></b>", result)
    authors_books.short_description = "Total Number Books"

    list_display_links = ('id', 'name', 'age',)
    list_per_page = 10
    save_as = True


# @admin.register(Publisher)
# class PublisherAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#     ordering = ['id']
#
#     fieldsets = [
#         ("Name", {"fields": ["name"], }),
#         # ('Email', {'fields': ['email', ], 'classes': ['wide', ]}),
#     ]
#
#     list_display_links = ('id', 'name',)
#     list_per_page = 10
#     save_as = True
#
#     class BookInLine(admin.TabularInline):
#         model = Book
#         extra = 1
#     inlines = [BookInLine]
#
#
# @admin.register(Store)
# class StoreAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#     ordering = ['id']
#
#     fieldsets = [
#         ("ID", {"fields": ['id'], }),
#         ("Name", {"fields": ['name'], }),
#         # ('Email', {'fields': ['email', ], 'classes': ['wide', ]}),
#     ]
#
#     list_display_links = ('id', 'name',)
#     list_per_page = 10
#     save_as = True
#
#
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'pages', 'price', 'rating', "publisher", "pubdate"]
#     ordering = ['id']
#
#     # def average_run_time(self, obj):
#     #     result = Logger.objects.filter(method=obj.method).aggregate(Avg("run_time"))
#     #     return format_html("<b><i>{}</i></b>", round(result["run_time__avg"], 7))
#     # average_run_time.short_description = "Average Method Run-Time"
#
#     list_filter = ('id', 'name', 'pages', 'price', 'rating', "publisher", "pubdate")
#     search_fields = ('id', 'name', 'pages', 'price', 'rating', "publisher", "pubdate")
#     fieldsets = (
#         ("Name", {
#             'fields': ('name',)
#         }),
#         ('Pages', {
#             'fields': ('pages',)
#         }),
#         ('Price', {
#             'fields': ('price',)
#         }),
#         ('Rating', {
#             'fields': ('rating',)
#         }),
#         ('Publisher', {
#             'fields': ('publisher',)
#         }),
#         ('Publication Date', {
#             'fields': ('pubdate',)
#         }),
#         # ('Advanced options', {
#         #     'fields': ('run_time',),
#         #     'classes': ('collapse', 'wide',),
#         # }),
#     )
#
#     date_hierarchy = 'pubdate'
#     actions_on_top = False
#     actions_on_bottom = True
#     actions_selection_counter = True  # By default
#     empty_value_display = '-empty-'
#     save_as = True
#     list_per_page = 10
#     list_display_links = ('id', 'name', 'pages', 'price', 'rating', 'publisher', 'pubdate')
#     filter_horizontal = ('authors',)
