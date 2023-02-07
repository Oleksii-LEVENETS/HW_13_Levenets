from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.template.defaultfilters import pluralize

from faker import Faker


class Command(BaseCommand):
    help = 'Creating fake Users'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('count_of_users', type=int, choices=range(1, 11),
                            help="Enter an integer from 1 to 10 incl. -- the count of fake users.")

    def handle(self, *args, **options):
        fake = Faker()
        list_users = []
        for u in range(options['count_of_users']):
            name = fake.name()
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[-1]
            username = first_name.lower() + last_name.lower()
            email = username + "@" + last_name.lower() + ".com"
            password = fake.password()
            list_users.append(User(username=username, password=make_password(password), email=email,
                                   first_name=first_name, last_name=last_name))

        User.objects.bulk_create(list_users)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {options['count_of_users']} "
                                             f"user{pluralize(options['count_of_users'])}!"))
