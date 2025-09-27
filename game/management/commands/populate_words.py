from django.core.management.base import BaseCommand
from game.models import Word


class Command(BaseCommand):
    help = 'Populate the database with initial 5-letter words'

    def handle(self, *args, **options):
        # List of 20 common 5-letter words
        words = [
            'ABOUT', 'ABOVE', 'ABUSE', 'ACTOR', 'ACUTE',
            'ADMIT', 'ADOPT', 'ADULT', 'AFTER', 'AGAIN',
            'AGENT', 'AGREE', 'AHEAD', 'ALARM', 'ALBUM',
            'ALERT', 'ALIEN', 'ALIGN', 'ALIKE', 'ALIVE'
        ]

        created_count = 0
        existing_count = 0

        for word in words:
            word_obj, created = Word.objects.get_or_create(word=word)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created word: {word}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Word already exists: {word}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} words created, {existing_count} words already existed'
            )
        )
