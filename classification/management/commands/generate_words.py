import os
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import Section, Program, Party

from classification import classes

class Command(BaseCommand):
    args = '<classifier name>'
    help = 'Classifies the sections'

    def handle(self, *args, **options):
        classifier_name = args[0]
        print classifier_name