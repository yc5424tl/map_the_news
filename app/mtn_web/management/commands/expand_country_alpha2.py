from django.core.management.base import BaseCommand
from mtn_web.models import Source
import pycountry


class Command(BaseCommand):
    help = 'Derives the display_name and alphanum_name for a given country by its alpha2_code'

    def handle(self, *args, **options):
        count = 0
        named_from_exception = 0
        sources = Source.objects.all().defer('country', 'language', 'name', 'languages', 'publishing_country', 'readership_countries', 'categories', 'url', 'verified')
        for source in sources:
            country_full_name = pycountry.countries.lookup(source.country_alpha2_code).name
            language_full_name = pycountry.languages.get(alpha_2=source.language_alpha2_code).name

            # COUNTRY DISPLAY NAME
            try:
                comma_index = country_full_name.find(',')
                if comma_index == -1:  # No Comma in country_full_name
                    source.country_display_name = country_full_name
                else:
                    '''
                    Substring up to first comma, i.e. "Bolivia, Plurinational State of" will return "Bolivia".
                    This is dont as the country names are used to:
                        - generate element id's in templates, and neither spaces or commas are allowed.

                        - As a user-friendly alternative to being presented iso-alpha2/3 codes in templates.

                

                    '''
                    substring = country_full_name[:comma_index]
                    source.country_display_name = substring
            except LookupError:
                source.country_display_name = country_full_name
                named_from_exception += 1

            # COUNTRY ALPHANUMERICAL NAME
            try:
                alphanum_filter = filter(str.isalnum, country_full_name)  # only alphanum chars remain
                alphanum_name = "".join(alphanum_filter)
                source.country_alphanum_name = alphanum_name
            except LookupError:
                source.country_alphanum_name = source.country_alpha2_code
                named_from_exception += 1

            # LANGUAGE DISPLAY NAME
            try:
                source.language_display_name = language_full_name
            except LookupError:
                source.language_display_name = source.language_alpha2_code
                named_from_exception += 1

            # LANGUAGE ALPHANUMERICAL NAME
            try:
                alphanum_filter = filter(str.isalnum, language_full_name)
                alphanum_name = "".join(alphanum_filter)
                source.language_alphanum_name = alphanum_name
            except LookupError:
                source.language_alphanum_name = source.language_alpha2_code
                named_from_exception += 1

            count += 1
        Source.objects.bulk_update(sources, ['language_alphanum_name', 'language_display_name', 'country_alphanum_name', 'country_display_name'], batch_size=2000)
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Expand Country Alpha2 (Successful: {count} Exceptions*: {named_from_exception} **up to 4/src**'))
