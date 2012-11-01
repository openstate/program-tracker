import os
import sys
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import Section, Program, Party

from classification import classes

class Command(BaseCommand):
    args = '<classifier name>'
    help = 'Generates a background model for the classifier'

    def handle(self, *args, **options):
        classifier_name = args[0]
        try:
            classifier_class = classes.AVAILABLE_CLASSIFIERS[classifier_name]
        except KeyError, e:
            classifier_class = None

        if classifier_class is None:
            classifier_list = u','.join(classes.AVAILABLE_CLASSIFIERS)
            print >>sys.stderr, "No classifier by such name found. Use one of : " + classifier_list
            sys.exit(1)

        classifier = classifier_class(preload=True)
        classifier.generate_similarity()
            