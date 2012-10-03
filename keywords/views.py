# -*- coding: utf-8 -*-
import json
import re
import shlex, subprocess, pickle, math

from pickle import dumps
from subprocess import CalledProcessError
from string import split, translate, maketrans, lower
from collections import defaultdict

from django.utils import simplejson
from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

from core.models import Party
from core.models import Section, SectionType
from core.models import Paragraph
from core.models import Program

from topic.models import Topic, Selection, Source

path = settings.PROJECT_DIR("algorithms") + "/"
algorithmname = "keywords"


def addSelections(request):
	common = set(x.strip().lower() for x in open(settings.PROJECT_DIR("words") + '/top100nl.txt'))
	
	for p in Party.objects.all():
		common.add(p.name.lower())
	
	wordlist = defaultdict(int)
	ttable = dict.fromkeys(map(ord, ',.;:()‘"\'?!@#$/*')+[0x201c, 0x201d, 0x2018, 0x2019, 0x2013], None)

	termfreqs = dict()
	paragraphs = Paragraph.objects.all().order_by('id')
	for p in paragraphs:
		termc = defaultdict(int)
		words = split(p.text.translate(ttable).lower())
		for word in words:
			if word in common:
				continue
			
			termc[word] += 1
		for word in termc.keys():
			wordlist[word] += 1
		
		termf = dict()
		if len(termc) > 0:
			maxcount = max(termc.values())
			for (word, count) in termc.items():
				termf[word] = float(count) / float(maxcount) 
		termfreqs[p.id] = termf
	
	idf = {}
	docnr = len(wordlist)
	for (word, count) in wordlist.items():
		idf[word] = math.log(docnr / count)
	
	for p in paragraphs:
		highest = ('',0)
		for item in termfreqs[p.id].items():
			if item[1] > highest[1]:
				highest = item
		if highest[1] > 0:		
			source, created = Source.objects.get_or_create(name = algorithmname)
		 
			t, created = Topic.objects.get_or_create(
				source = source,
				description = str(highest[1]), 
				name = highest[0])
						
			s = Selection.objects.create(
				source = source,
				paragraph = p,
				startLetter = 0,
				endLetter = -1,
				user = None,
				topic = t,)
				
	return HttpResponse('done', 'text/plain')

def clear(request):
	Selection.objects.filter(source__name=algorithmname).delete()
	Topic.objects.filter(source__name=algorithmname).delete()
	return HttpResponse('done', 'text/plain')
