from django.core.management.base import BaseCommand
from mtn_web.models import Source


class Command(BaseCommand):
    help = "transfers all country and language alpha2 codes to new (better named) columns, allowing the repurposing of the original columns"

    def handle(self, *args, **options):
        count = 0
        sources = Source.objects.all().only('country_alpha2_code', 'language_alpha2_code', 'country', 'language')
        for source in sources:
            source.country_alpha2_code = source.country
            source.language_alpha2_code = source.language
            count += 1
        Source.objects.bulk_update(sources, ['country_alpha2_code', 'language_alpha2_code'], batch_size=2000)
        self.stdout.write(self.style.SUCCESS(f'COMPLETE - Transfer Alpha2 To New Columns (Total: {count})'))
