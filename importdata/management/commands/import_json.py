import os
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import Section, Program, Party
from importdata.utils import import_json_program


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        files = os.listdir(settings.PROJECT_DIR("programmas"))
        for file in files:
            print file
            party_name, dummy = os.path.splitext(os.path.basename(file))
            party, was_created = Party.objects.get_or_create(
                name=party_name
            )
            section, was_created = Section.objects.get_or_create(
                name=os.path.basename(file)
            )
            program, was_created = Program.objects.get_or_create(
                date=datetime.datetime.now().date(),
                party=party,
                name='programma %s' % (party_name, )
            )
            import_json_program(party_name, program.pk)