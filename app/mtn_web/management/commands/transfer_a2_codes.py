from django.core.management.base import BaseCommand
from mtn_web.models import Source


class Command(BaseCommand):
    help = "transfers all country and language alpha2 codes to new (better named) columns, allowing the repurposing of the original columns"

    def handle(self, *args, **options):
        count = 0
        for source in Source.objects.all().only('country_alpha2_code', 'language_alpha2_code', 'country', 'language'):
            source.country_alpha2_code = source.country
            source.language_alpha2_code = source.language
            source.save()
            count += 1
            # self.stdout.write(self.style.SUCCESS(f'Successfully transfered alpha2 codes to new columns -- record {count}'))
        self.stdout.write(self.style.SUCCESS(f'COMPLETE - Transfer Alpha2 To New Columns (Total: {count})'))
