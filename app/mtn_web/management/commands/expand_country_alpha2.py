from django.core.management.base import BaseCommand
from mtn_web.models import Source
import pycountry


class Command(BaseCommand):
    help = 'Derives the display_name and alphanum_name for a given country by its alpha2_code'

    def handle(self, *args, **options):
        count = 0
        for source in Source.objects.all():

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
                    country_full_name      - As a user-friendly alternative to being presented iso-alpha2/3 codes in templates.
                    '''
                    substring = country_full_name[:comma_index]
                    source.country_display_name = substring
                    # source.save()
            except LookupError:
                source.country_display_name = country_full_name
                # source.save()
            # COUNTRY ALPHANUMERICAL NAME
            try:
                alphanum_filter = filter(str.isalnum, country_full_name)  # only alphanum chars remain
                alphanum_name = "".join(alphanum_filter)
                source.country_alphanum_name = alphanum_name
                # source.save()
            except LookupError:
                source.country_alphanum_name = source.country_alpha2_code
                # source.save()
            # LANGUAGE DISPLAY NAME
            try:
                source.language_display_name = language_full_name
                # source.save()
            except LookupError:
                source.language_display_name = source.language_alpha2_code
                # source.save()
            # LANGUAGE ALPHANUMERICAL NAME
            try:
                alphanum_filter = filter(str.isalnum, language_full_name)
                alphanum_name = "".join(alphanum_filter)
                source.language_alphanum_name = alphanum_name
                # source.save()
            except LookupError:
                source.language_alphanum_name = source.language_alpha2_code
                # source.save()
            source.save()
            count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully Expanded alpha2 for Record {count}"))
