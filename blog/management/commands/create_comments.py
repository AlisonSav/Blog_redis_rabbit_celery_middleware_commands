from datetime import datetime
from random import randint

from django.core.management.base import BaseCommand

from faker import Faker

from blog.models import Comment


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of Comments to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")
        Comment.objects.bulk_create(
            Comment(
                post_id=randint(1, 33),
                author=fake.user_name(),
                comment_text=fake.sentence(),
                is_published=randint(0, 1),
                created_on=datetime.utcnow(),
            )
            for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Comments"))
