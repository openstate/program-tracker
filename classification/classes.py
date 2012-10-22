#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from pprint import pprint

from gensim import corpora, models, similarities
 
from django.conf import settings

from core.models import Party, Program, Section, Paragraph


class WordSplitter(object):
    common_words = []
    word_delimiters = []

    def __init__(self):
        self.common_words = set(
            x.strip().lower() for x in open(settings.PROJECT_DIR("words") + '/top10000nl.txt')
        )
        for p in Party.objects.all():
        	self.common_words.add(p.name.lower())
        self.word_delimiters = dict.fromkeys(map(ord, ',.;:()‘"\'?!@#$/*')+[0x201c, 0x201d, 0x2018, 0x2019, 0x2013], None)

    def split(self, paragraph):
        words = [
            word for word in paragraph.text.translate(self.word_delimiters).lower().split(
            ) if word not in self.common_words
        ]
        return words


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
        print >>sys.stderr, "Initializing lda classifier ..."

    # options is not random etc.
    def generate_background_model(self, options = {}):
        print >>sys.stderr, "Generating background model ..."
        splitter = WordSplitter()
        docs = []
    	for p in Paragraph.objects.all().order_by('id')[:10]:
            docs.append(splitter.split(p))
    	pprint(docs)

    def classify(self, paragraph, options = {}):
        raise NotImplementedError

AVAILABLE_CLASSIFIERS = {
    u"lda": LDAClassifier,
}