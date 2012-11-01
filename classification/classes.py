#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import codecs
from pprint import pprint
from string import lower

from pattern.nl import ngrams, parse

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

class PatternParagraphSplitter(object):
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
        '''
        We use pattern.nl to tokenize and stem all the words
        '''
        parsed_words = parse(lower(paragraph.text.strip()), lemmata=True).split(' ')
        if parsed_words == ['']:
            return []

        try:
            stemmed_words = map(lambda x: x.split('/')[4] , parsed_words)
        except Exception:
            pass
        stemmed_paragraph = ' '.join(stemmed_words)
        onegrams = ngrams(stemmed_paragraph, n=1)

        return [ word[0] for word in onegrams if word[0] not in self.common_words ]


class ParagraphCorpus(object):
    splitter = None
    dictionary = None
    docs = []

    def __init__(self, splitter, dictionary, docs):
        self.splitter = splitter
        self.dictionary = dictionary
        self.docs = docs

    def __iter__(self):
        for d in self.docs:
            yield self.dictionary.doc2bow(d)


class AbstractClassifier(object):
    name = 'abstract'
    splitter = None
    dictionary = None
    corpus = None
    model = None
    modelClass= None
    options = {}


    def __init__(self, preload=False, options = {}):
        print >>sys.stderr, "Initializing classifier ..."

        self.options = options

        if preload:
            print >>sys.stderr, "Loading dictory ..."
            self.dictionary = corpora.Dictionary.load(settings.PROJECT_DIR('classification') + '/' + self.name + '.dict')
            #pprint(self.dictionary.token2id)
            
            print >>sys.stderr, "Loading corpus ..."
            self.corpus = corpora.MmCorpus(settings.PROJECT_DIR('classification') + '/' + self.name + '.mm')
            
            print >>sys.stderr, "Loading model ..."
            self.model = self.modelClass.load(settings.PROJECT_DIR('classification') + '/' + self.name + '.model')



    # options is not random etc.
    def generate_background_model(self):
        print >>sys.stderr, "Generating background model ..."
        docs = self.split(self.get_docs())     
        self.dictionary = self.generate_dictionary(docs)
        self.corpus = self.generate_corpus(docs)
        self.model = self.train()
        self.save()

    def get_docs(self):
        raise NotImplementedError

    def split(self, texts):
        # generate a list of words ...
        docs = []
        for p in texts:
            docs.append(self.splitter.split(p))
        return docs

    def generate_dictionary(self, docs):
        '''make a dictionary and save it'''
        print >>sys.stderr, "Generating dictionary ..."
        dictionary = corpora.Dictionary(docs)
        #pprint(dictionary.token2id)
        dictionary.save(settings.PROJECT_DIR('classification') + '/' + self.name + '.dict')
        return dictionary


    def generate_corpus(self, docs):
        '''make a corpus and save it to disk ...'''
        print >>sys.stderr, "Generating corpus ..."
        corpus = ParagraphCorpus(self.splitter, self.dictionary, docs)
        corpora.MmCorpus.serialize(settings.PROJECT_DIR('classification') + '/' + self.name + '.mm', corpus)

    def train(self):
        raise NotImplementedError

    def save(self):
        self.model.save(settings.PROJECT_DIR('classification') + '/' + self.name + '.model')


    def classify(self, paragraph):
        raise NotImplementedError


    def get_doc_model(self, paragraph):
        split_text = self.splitter.split(paragraph)
        vector = self.dictionary.doc2bow(split_text)
        return self.model[vector]


  
    def _link_paragraph_to_topic(self, paragraph, topics):
        source, created = Source.objects.get_or_create(
            name=self.name
        )

        selections = []
        for topic_data in topics:
            name = topic_data['name'] if 'name' in topic_data else None 
            description = topic_data['description'] if 'description' in topic_data else None

            topic, created = Topic.objects.get_or_create(
                name=name,
                source=source,
                description=description
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

    def generate_similarity(self):
        print >>sys.stderr, "Generating index ..."
        index = similarities.MatrixSimilarity(self.corpus)
        index.save(settings.PROJECT_DIR('classification') + '/' + self.name + '.index')
        return index

    def get_similar_documents(self, query):
        doc_model = self.get_doc_model(query)
        sims = self.index[doc_model]

    def query(self, query, number):
        pass

class LDAClassifier(AbstractClassifier):
    name = 'lda'
    modelClass = models.ldamodel.LdaModel
    splitter = PatternParagraphSplitter()
  
    def get_docs(self):
        return Paragraph.objects.all().order_by('id')

    def generate_dictionary(self, docs):
        dictionary = super(LDAClassifier, self).generate_dictionary(docs)

        #filter extremes (minimal 2 paragraphs, top 0.5 removed)
        dictionary.filter_extremes(no_below=2, no_above=0.5)

        # save again since we changed it
        dictionary.save(settings.PROJECT_DIR('classification') + '/' + self.name + '.dict')
        return dictionary 

    # options is not random etc.
    def train(self):
        # now train the classifier ...
        print >>sys.stderr, "Generating lda model ..."
        lda = models.ldamodel.LdaModel(
            corpus=self.corpus, id2word=self.dictionary, num_topics=20, update_every=0, passes=20
        )

        return lda

    def classify(self, paragraph):
        doc_model = self.get_doc_model(paragraph)
        #print doc_lda
        if len(doc_model) > 1:
            topic_id, prob = doc_model[0] # take the highest one
            topic = self.model.show_topic(topic_id)
            name = 'Topic %s' % topic_id
            description = self.model.print_topic(topic_id)
            self._link_paragraph_to_topic(
                paragraph=paragraph,
                topics=[{'name':name, 'description': description}]
            )


AVAILABLE_CLASSIFIERS = {
    u"lda": LDAClassifier,
}