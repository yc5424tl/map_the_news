from mtn_web.models import Source, Language
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Used for migrating data out of the Source model into a new Language model"

    def handle(self, *args, **options):
        languages = Source.objects.values('language_alpha2_code', 'language_display_name', 'language_alphanum_name').distinct().iterator()
        instance_list = []

        for language_data in languages:
            new_language = Language(
                alpha2_code=language_data['language_alpha2_code'],
                display_name=language_data['language_display_name'],
                alphanum_name=language_data['language_alphanum_name']
            )
            instance_list.append(new_language)

        Language.objects.bulk_create(instance_list)
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Populate Languages From Sources (Added: {len(instance_list)} Language(s))'))
