#!/usr/bin/env python

import sys
import os
import re

from django.conf import settings

from core.models import Party, Program, Section, Paragraph

class AbstractClassifier(object):
    def __init__(self):
        pass

    # options is not random etc.
    def generate_background_model(self, options = {}):
        raise NotImplementedError

    def classify(self, paragraph, options = {}):
        raise NotImplementedError


class LDAClassifier(AbstractClassifier):
    def __init__(self):
        pass

    # options is not random etc.
    def generate_background_model(self, options = {}):
        raise NotImplementedError

    def classify(self, paragraph, options = {}):
        raise NotImplementedError

AVAILABLE_CLASSIFIERS = {
    u"lda": LDAClassifier,
}