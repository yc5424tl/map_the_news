from django.core.management.base import BaseCommand
from mtn_web.models import Source, Language
from django.db.models import Prefetch


class Command(BaseCommand):
    help = "Used as part of moving language and country data out of the Source model. This command is used to (re)build the relations between sources and languages."

    def handle(self, *args, **options):
        count = 0
        language_mapper = {}

        for language in Language.objects.all():
            language_mapper[language.alpha2_code] = language

        for source in Source.objects.only('language', 'languages').prefetch_related(Prefetch('languages', queryset=Language.objects.all())).iterator():
            if language_mapper[source.language] not in source.languages.all():
                source.languages.add(language_mapper[source.language])
                count += 1

        self.stdout.write(self.style.SUCCESS(f'COMPLETE -- Established Source Language Relations ({count})'))
