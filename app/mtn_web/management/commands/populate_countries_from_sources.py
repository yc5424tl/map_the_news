from mtn_web.models import Source, Country
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Used for migrating data out of the Source model into a new Country model."

    def handle(self, *args, **options):
        countries = Source.objects.values('country_alpha2_code', 'country_display_name', 'country_alphanum_name').distinct()
        instance_list = []
        for country_data in countries:
            country = Country(
                alpha2_code=country_data['country_alpha2_code'],
                display_name=country_data['country_display_name'],
                alphanum_name=country_data['country_alphanum_name']
            )
            instance_list.append(country)

        Country.objects.bulk_create(instance_list)
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Populate Countries From Sources (Added: {len(instance_list)} Countries)'))


'''
    # def handle(self, *args, **options):
    #     count = 0
    #     skipped = 0
    #     countries = Source.objects.values('country_alpha2_code', 'country_display_name', 'country_alphanum_name').distinct()
    #     for country_data in countries:
    #         country, created = Country.objects.get_or_create(
    #             alpha2_code=country_data['country_alpha2_code'],
    #             display_name=country_data['country_display_name'],
    #             alphanum_name=country_data['country_alphanum_name']
    #         )
    #         if created:
    #             count += 1
    #             # self.stdout.write(self.style.SUCCESS(f"New Country Added: {new_country.display_name} (No. {count})"))
    #         else:
    #             skipped += 1
    #             # self.stdout.write(self.style.SUCCESS(f'Country Exists in Database, NOT CREATED {country_data["country_display_name"]}'))
    #     self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Populate Countries From Sources  (Added: {count}  Skipped: {skipped})'))
'''
