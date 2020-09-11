from django.core.management.base import BaseCommand
from mtn_web.models import Source, Country


class Command(BaseCommand):
    help = "Final Step in moving country data out of Source in to Country, this command establishes the new foreign key relationships between Source and Country for existing records."

    def handle(self, *args, **options):

        count = 0
        exceptions = 0
        sources = Source.objects.all().only('country_alpha2_code', 'publishing_country')

        for source in sources:
            alpha2_code = source.country_alpha2_code
            try:
                source.publishing_country = Country.objects.get(alpha2_code=alpha2_code)
                count += 1
            except Country.DoesNotExist:
                exceptions += 1
                self.stdout.write(self.style.NOTICE(f'Country.DoesNotExist exception from alpha2={alpha2_code} for source={source.name}'))

        Source.objects.bulk_update(sources, ['publishing_country'], batch_size=2000)
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Established Source Publishing Country Relations (Successful: {count}  Exceptions: {exceptions})'))
