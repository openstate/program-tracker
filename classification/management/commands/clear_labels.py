import os
import sys
import datetime

from django.core.management.base import BaseCommand, CommandError

from topic.models import Source

class Command(BaseCommand):
    args = '<source name>'
    help = 'Clears added labels for source'

    def handle(self, *args, **options):
        name = args[0]
        try:
            sources = Source.objects.filter(name=name)
        except Source.DoesNotExist:
            print >>sys.stderr, "No source by such name found."
        else:
            sources.delete()

        
            