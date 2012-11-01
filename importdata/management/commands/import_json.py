import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import Section, Program, Party, SectionType
from importdata.utils import import_json_program


class Command(BaseCommand):
    args = '<yyyy-mm-dd>'
    help = 'Imports json programmes from "programmas" directory'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Not the right amount of arguments')
        try:
            election_date = datetime.strptime(args[0], '%Y-%m-%d').date()
        except Exception as exception:
            raise CommandError('Not the correct date format: %s' % exception)

        files = os.listdir(settings.PROJECT_DIR("programmas"))
        for file in files:
            print file
            party_name, dummy = os.path.splitext(os.path.basename(file))
            party, was_created = Party.objects.get_or_create(
                name__iexact=party_name
            )
            import_json_program(party_name, party, election_date)