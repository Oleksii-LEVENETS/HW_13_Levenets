import random

from aggregation.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):
    help = 'Creating fake 10 Authors, 10 Publishers, 500 Books, 10 Stores'  # noqa: A003

    def handle(self, *args, **options):
        fake = Faker()
        list_authors = []
        list_publishers = []
        list_books = []
        list_stores = []

        # Creating 10 Authors and 10 Publishers
        for _ in range(10):
            author_name = fake.name()
            author_age = fake.random_int(20, 110)
            list_authors.append(Author(name=author_name, age=author_age,))

            publisher_name = fake.word().upper()
            list_publishers.append(Publisher(name=publisher_name,))

        Author.objects.bulk_create(list_authors)
        Publisher.objects.bulk_create(list_publishers)

        authors_id = Author.objects.values_list('id', flat=True)
        publisher_id = Publisher.objects.values_list('id', flat=True)

        # Creating 1000 Books
        for _ in range(500):
            book_name = fake.text(18)
            book_pages = random.randint(50, 500)
            book_price = round((random.randint(100, 10_000) / random.randint(10, 100)), 2)
            book_rating = round((10 / random.randint(1, 10)), 2)
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

        # Creating M2M Book-Author
        for book in books_created:
            authors_list = []
            for _ in range(random.choice([1, 2])):
                authors_list.append(random.choice(authors_id))
            if len(authors_list) > 1:
                book.authors.add(authors_list[0], authors_list[1])
            book.authors.add(authors_list[0])

        # Creating 10 Stores
        for _ in range(10):
            store_name = fake.word().capitalize()
            list_stores.append(Store(name=store_name,))

        stores_created = Store.objects.bulk_create(list_stores)

        # Creating M2M Store-Book
        for store in stores_created:
            books_list = []
            quantity_books = random.randint(200, 499)
            for _ in range(quantity_books):
                books_list.append(random.choice(books_id))

            books_list = list(set(books_list))
            store.books.set(books_list)

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created fake 10 Authors, 10 Publishers, 500 Books, 10 Stores"))
