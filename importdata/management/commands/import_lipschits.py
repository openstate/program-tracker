import os
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from importdata.utils import import_lipschits


class Command(BaseCommand):
    args = '<year>'
    help = 'Imports xml programmes from "LipschitsBooksinXML" directory'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Not the right amount of arguments')
        try:
            election_year = int(args[0])
        except Exception as exception:
            raise CommandError('Not the correct year format: %s' % exception)
        else:
            import_lipschits(election_year)