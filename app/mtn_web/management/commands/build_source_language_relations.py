from django.core.management.base import BaseCommand
from mtn_web.models import Source, Language


class Command(BaseCommand):
    help = "Used as part of moving language and country data out of the Source model. This command is used to (re)build the relations between sources and languages."

    def handle(self, *args, **options):
        count = 0
        language_mapper = {}

        for language in Language.objects.all():
            language_mapper[language.alpha2_code] = language

        for source in Source.objects.all().only('language', 'languages').iterator():
            alpha2_code = source.language
            language_object = language_mapper[alpha2_code]
            if language_object not in source.languages.all():
                source.languages.add(language_object)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Established Source Language Relations ({count})'))
