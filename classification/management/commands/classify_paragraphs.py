import os
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import Section, Program, Party


class Command(BaseCommand):
    args = ''
    help = 'Classifies the sections'

    def handle(self, *args, **options):
        pass