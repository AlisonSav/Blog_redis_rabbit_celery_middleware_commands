from datetime import datetime
from random import randint

from django.core.management.base import BaseCommand

from faker import Faker

from blog.models import Post


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of Posts to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")
        Post.objects.bulk_create(
            Post(
                author_id=randint(1, 24),
                title=fake.company(),
                description=fake.sentence(),
                body=fake.text(),
                is_published=randint(0, 1),
                created_on=datetime.utcnow(),
            )
            for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Posts"))
