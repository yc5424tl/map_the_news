from django.core.management.base import BaseCommand
from mtn_web.models import Source, Country


class Command(BaseCommand):
    help = 'Transfering the adhoc original_country.original_language data placed in some of the Source objects url field into the new readership_countries field.'

    def handle(self, *args, **options):
        count = 0
        skipped = 0
        exceptions = 0
        for source in Source.objects.exclude(url__isnull=True).exclude(url__exact='').extra(where=["CHAR_LENGTH(url) = 12"]):
            alpha2_code = source.url[7:9]
            try:
                country_object = Country.objects.get(alpha2_code=alpha2_code)
                if country_object not in source.readership_countries.all():
                    source.readership_countries.add(country_object)
                    source.save()
                    count += 1
                    # self.stdout.write(self.style.SUCCESS(f'Added Country.alpha2={country_object.alpha2_code} to Source.readership_countries from alpha2={alpha2_code} (No. {count})'))
                else:
                    skipped += 1
            except Country.DoesNotExist:
                exceptions += 1
                self.stdout.write(self.style.SUCCESS(f'Country.DoesNotExist on Alpha2={alpha2_code} for Source={source.name}'))
                # self.stdout.write(self.style.SUCCESS(f'{country_object.display_name} already listed as readership country for {source.name}'))
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Established Source Readership Country Relations (Added: {count}  Skipped: {skipped})'))
