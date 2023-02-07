import random

from aggregation.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand
from django.template.defaultfilters import pluralize

from faker import Faker


class Command(BaseCommand):
    help = 'Creating fake Authors, Publishers, Books, Stores'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('count_of_new_models', type=int, choices=range(1, 11),
                            help="Enter an integer from 1 to 10 incl. -- the count of new models respectively.")

    def handle(self, *args, **options):
        num = options['count_of_new_models']
        fake = Faker()
        list_authors = []
        list_publishers = []
        list_books = []
        list_stores = []

        for _ in range(num):
            author_name = fake.name()
            author_age = fake.random_int(20, 110)
            list_authors.append(Author(name=author_name, age=author_age,))

            publisher_name = "Publisher " + fake.word().upper()
            list_publishers.append(Publisher(name=publisher_name,))

        Author.objects.bulk_create(list_authors)
        Publisher.objects.bulk_create(list_publishers)

        authors_id = Author.objects.values_list('id', flat=True)
        publisher_id = Publisher.objects.values_list('id', flat=True)

        for _ in range(num):
            book_name = fake.text(18)
            book_pages = fake.random_int(50, 1000)
            book_price = round((fake.random_int(100, 1000) / fake.random_int(50, 100)), 2)
            book_rating = round((10 / fake.random_int(1, 10)), 2)
            pubdate = fake.date_of_birth()
            list_books.append(Book(
                name=book_name,
                pages=book_pages,
                price=book_price,
                rating=book_rating,
                pubdate=pubdate,
                publisher=Publisher.objects.get(pk=random.choice(publisher_id)),
                )
            )

        books_created = Book.objects.bulk_create(list_books)
        books_id = Book.objects.values_list('id', flat=True)

        for book in books_created:
            authors_list = []
            for _ in range(fake.random_int(1, 2)):
                authors_list.append(random.choice(authors_id))
            if len(authors_list) > 1:
                book.authors.add(authors_list[0], authors_list[1])
            book.authors.add(authors_list[0])

        for _ in range(num):
            store_name = "Store " + fake.word().capitalize()
            list_stores.append(Store(
                name=store_name,
                )
            )

        stores_created = Store.objects.bulk_create(list_stores)

        for store in stores_created:
            books_list = []
            quantity_books = fake.random_int(1, len(books_id))
            for _ in range(quantity_books):
                books_list.append(random.choice(books_id))

            books_list = list(set(books_list))
            store.books.set(books_list)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {options['count_of_new_models']} "
                                             f"new model{pluralize(options['count_of_new_models'])}!"))
