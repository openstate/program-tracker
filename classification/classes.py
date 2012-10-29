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
from topic.models import Source, Topic, Selection

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
    def __init__(self, preload=False):
        pass

    # options is not random etc.
    def generate_background_model(self, options = {}):
        raise NotImplementedError

    def classify(self, paragraph, options = {}):
        raise NotImplementedError

    def _link_paragraph_to_topic(self, paragraph, source_name, topic_names):
        source, created = Source.objects.get_or_create(
            name=source_name
        )

        selections = []
        for topic_name in topic_names:
            topic, created = Topic.objects.get_or_create(
                name=topic_name,
                source=source,
                description =topic_name
            )

            selection = Selection.objects.get_or_create(
                source=source,
                paragraph=paragraph,
                startLetter=0,
                endLetter=-1,
                user=None,
                topic=topic,
            )
            selections.append(selection)
        
        return selections

class LDAClassifier(AbstractClassifier):
    dictionary = None
    lda = None
    splitter = None

    def __init__(self, preload=False):
        print >>sys.stderr, "Initializing lda classifier ..."
        if preload:
            print >>sys.stderr, "Loading dictory ..."
            self.dictionary = corpora.Dictionary.load(settings.PROJECT_DIR('classification') + '/lda.dict')
            #pprint(self.dictionary.token2id)
            print >>sys.stderr, "Loading LDA model ..."
            self.lda = models.ldamodel.LdaModel.load(settings.PROJECT_DIR('classification') + '/lda.model')
            print >>sys.stderr, "Initializing splitter ..."
            self.splitter = ParagraphSplitter()
            
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
        doc_lda = self.lda[self.dictionary.doc2bow(self.splitter.split(paragraph))]
        #print doc_lda
        if len(doc_lda) > 1:
            topic_id, prob = doc_lda[0] # take the highest one
            topic = self.lda.show_topic(topic_id)
            topic_name = topic[0][1]
            self._link_paragraph_to_topic(
                paragraph=paragraph,
                source_name="lda",
                topic_names=[topic_name]
            )
        

AVAILABLE_CLASSIFIERS = {
    u"lda": LDAClassifier,
}