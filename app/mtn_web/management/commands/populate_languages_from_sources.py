from mtn_web.models import Source, Language
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Used for migrating data out of the Source model into a new Language model"

    def handle(self, *args, **options):
        count = 0
        skipped = 0
        languages = Source.objects.values('language_alpha2_code', 'language_display_name', 'language_alphanum_name').distinct()
        for language_data in languages:
            language, created = Language.objects.get_or_create(
                alpha2_code=language_data['language_alpha2_code'],
                display_name=language_data['language_display_name'],
                alphanum_name=language_data['language_alphanum_name']
            )
            if created:
                count += 1
                # self.stdout.write(self.style.SUCCESS(f"New Language Added: {new_language.display_name} -- {new_language.alpha2_code} (No. {count})"))
            else:
                skipped += 1
                # self.stdout.write(self.style.SUCCESS(f"Language Already Present - NOT ADDED TO DB @ {language_data['language_display_name']}"))
        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Populate Languages From Sources  (Added: {count}  Skipped: {skipped})'))
