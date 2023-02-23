from aggregation.tasks import tasks

from core.celery import app

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creating fake 10 Authors, 10 Publishers, 1'500 Books, 10 Stores"  # noqa: A003

    def handle(self, *args, **options):
        inspector = app.control.inspect().stats()
        if not inspector:
            self.stderr.write("Not successfully. Is it all ok with Celery?")
            exit()

        tasks.creating_new_models.delay()
        self.stdout.write(self.style.SUCCESS(
            "Successfully created fake 10 Authors, 10 Publishers, 1'500 Books, 10 Stores"))
