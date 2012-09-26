# -*- coding: utf-8 -*-
from django.template import Context, loader
from core.models import Party
from core.models import Section, SectionType
from core.models import Paragraph
from core.models import Program
from topic.models import Topic, Selection, Source
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
import json, os, glob
import re
import shlex, subprocess, pickle
from pickle import dumps
from subprocess import CalledProcessError
from string import split, translate, maketrans, lower
from django.utils import simplejson
from collections import defaultdict

path = "/home/hiram/program-tracker/algorithms/"
algorithmname = "sicco"


def words(request):
	
	for p in Party.objects.all():
		common.add(p.name.lower())
	
	ttable = dict.fromkeys(map(ord, ',.;:()‘"\'?!@#$/*')+[0x201c, 0x201d, 0x2018, 0x2019, 0x2013], None)

	for p in Paragraph.objects.all().order_by('id'):
		text = p.text.translate(ttable).lower()
		result.append({"id": p.id, "text":text})
	pickle = dumps(result)
				
	return HttpResponse(pickle, 'text/plain')

def addSelections(request):
	response = ""
	for p in Paragraph.objects.all().order_by('id'):
		file = open(path + "sicco/results/" + str(p.id) + ".txt")
#		topic = ' '.join(map(lambda x:x.split(' ')[2], file.readlines()[0:1]))
		topic = file.readline().split(' ')[2]

		source, created = Source.objects.get_or_create(name = algorithmname)

		t, created = Topic.objects.get_or_create(
				name = topic,
				source = source)
		
		s = Selection.objects.create(
				source = source,
				paragraph = p,
				startLetter = 0,
				endLetter = -1,
				topic = t,)
	return HttpResponse(response, 'text/plain')

def clear(request):
	Selection.objects.filter(source__name=algorithmname).delete()
	Topic.objects.filter(source__name=algorithmname).delete()
	return HttpResponse('done', 'text/plain')


def topics(request):
	p = Paragraph.objects.all()[0]
	file = open(path + "sicco/results/" + str(p.id) + ".txt")
	message = "\n".join(map(lambda x:x.split(' ')[2], file))

	return HttpResponse(message, 'text/plain')
