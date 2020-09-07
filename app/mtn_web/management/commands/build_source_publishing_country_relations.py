from django.core.management.base import BaseCommand
from mtn_web.models import Source, Country


class Command(BaseCommand):
    help = "Final Step in moving country data out of Source in to Country, this command establishes the new foreign key relationships between Source and Country for existing records."

    def handle(self, *args, **options):
        count = 0
        exceptions = 0
        for source in Source.objects.all().only('country_alpha2_code', 'publishing_country'):
            alpha2_code = source.country_alpha2_code
            try:
                source.publishing_country = Country.objects.get(alpha2_code=alpha2_code)
                # country_pk = Country.objects.get(alpha2_code=alpha2_code).pk
                # source.publishing_country = Country.objects.get(pk=country_pk)
                source.save()
                count += 1
            except Country.DoesNotExist:
                exceptions += 1
                self.stdout.write(self.style.NOTICE(f'Country.DoesNotExist exception from alpha2={alpha2_code} for source={source.name}'))
            # self.stdout.write(self.style.SUCCESS(f'Established Relation for {source.name}.alpha2_code={source.country_alpha2_code} to Country.alpha2_code={Country.objects.get(pk=country_pk).alpha2_code} (No. {count})'))
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Established Source Publishing Country Relations (Successful: {count}  Exceptions: {exceptions})'))
