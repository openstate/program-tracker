#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import codecs
from pprint import pprint

from gensim import corpora, models, similarities
 
from django.conf import settings

from core.models import Party, Program, Section, Paragraph


class ParagraphSplitter(object):
    common_words = []
    word_delimiters = []

    def __init__(self):
        self.common_words = set(
            x.strip().lower() for x in codecs.open(settings.PROJECT_DIR("words") + '/top10000nl.txt', 'r', 'iso-8859-1')
        )
        for p in Party.objects.all():
        	self.common_words.add(p.name.lower())
        self.word_delimiters = dict.fromkeys(map(ord, ',.;:()‘"\'?!@#$/*')+[0x201c, 0x201d, 0x2018, 0x2019, 0x2013], None)

    def split(self, paragraph):
        words = [
            unicode(word) for word in paragraph.text.translate(self.word_delimiters).lower().split(
            ) if word not in self.common_words
        ]
        return words


class ParagraphCorpus(object):
    splitter = None
    dictionary = None

    def __init__(self, splitter, dictionary):
        self.splitter = splitter
        self.dictionary = dictionary

    def __iter__(self):
    	for p in Paragraph.objects.all().order_by('id'):
            yield self.dictionary.doc2bow(self.splitter.split(p))


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

        # generate a list of words ...
        splitter = ParagraphSplitter()
        docs = []
    	for p in Paragraph.objects.all().order_by('id'):
            docs.append(splitter.split(p))

    	#pprint(docs)
    	dictionary = corpora.Dictionary(docs)
    	#pprint(dictionary.token2id)
        dictionary.save(settings.PROJECT_DIR('classification') + '/lda.dict')

        # make a corpus and save it ot disk ...
        corpus = ParagraphCorpus(splitter, dictionary)
        corpora.MmCorpus.serialize(settings.PROJECT_DIR('classification') + '/lda.mm', corpus)

        # now train the classifier ...
        lda = models.ldamodel.LdaModel(
            corpus=corpus, id2word=dictionary, num_topics=100, update_every=0, passes=20
        )
        lda.save(settings.PROJECT_DIR('classification') + '/lda.model')

    def classify(self, paragraph, options = {}):
        raise NotImplementedError

AVAILABLE_CLASSIFIERS = {
    u"lda": LDAClassifier,
}