# -*- coding: utf-8 -*-
from django.template import Context, loader
from core.models import Party
from core.models import Section, SectionType
from core.models import Paragraph
from core.models import Program
from topic.models import Topic, Selection, Source
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
import json
import re
import shlex, subprocess, pickle
from subprocess import CalledProcessError
from string import split, translate, maketrans, lower
from django.utils import simplejson
from collections import defaultdict

path = "/home/hiram/program-tracker/algorithms/"
algorithmname = "lda"
common = set(x.strip().lower() for x in open('/home/hiram/program-tracker/top1000nl.txt'))
for p in Party.objects.all():
		 common.add(p.name.lower())
ttable = dict.fromkeys(map(ord, ',.;:()‘"\'?!@#$/*')+[0x201c, 0x201d, 0x2018, 0x2019, 0x2013], None)



def words(request):
	
	
	wordlist = []
	result = []
	totalcount = 0

	for p in Section.objects.all().order_by('id'):
		wordlist, r = textToCounts(wordlist, p.text)
		result.append(r)
		totalcount += r['number']
		
	words = u"\n".join(wordlist).encode('utf-8')
	counts = render_to_response('core/counts.html', {"counts": result}).content

	fwords = open(path + 'data/words.txt','w')
	fwords.write(str(totalcount) + "\n" + words)
	fwords.close()
	
	fcounts = open(path + 'data/words.dat','w')
	fcounts.write(counts)
	fcounts.close()
	
	command = path + "lda-c-dist/hdp est 0.05 100 " + path + "lda-c-dist/settings.txt " + path + "data/words.dat " + path + "data/result/final " + path + "data/result"
	result = command
	try:
		pipe = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
		result += pipe
	except CalledProcessError as e:
		result += "\n" + str(e.returncode)
		result += "\n" + e.output
	
	#make_topics(path + "data/result/final.beta", path + "data/words.txt")
			
	return HttpResponse(result, 'text/plain')

def make_topics(beta_file, vocab_file, nwords = 25):

	# get the vocabulary

	vocab = file(vocab_file, 'r').readlines()
	# vocab = map(lambda x: x.split()[0], vocab)
	vocab = map(lambda x: x.strip(), vocab)

	# for each line in the beta file

	indices = range(len(vocab))
	topics = []

	for topic in file(beta_file, 'r'):
		topic = map(float, topic.split())
		topiclen = len(topic)
		topicl = []
		indices.sort(lambda x,y: -cmp(topic[x], topic[y]))
		for i in range(nwords):
			topicl.append(vocab[indices[i]])
		topics.append(topicl)
	pickle.dump(topics, open(path + "data/result/topics.pickle", 'w'))

def textToCounts(wordlist, text):
	result = defaultdict(int)
	words = split(text.translate(ttable).lower())
		
	for word in words:
			if word in common:
				continue
			
			wordlist, index = getwordIndex(wordlist, word)
			result[index] += 1 
	return (wordlist, {"number": len(result), "pcounts": result.items})

def getTopics():
	return pickle.load(open(path + "data/result/topics.pickle"))
		
def getTTopics():
	lines = open(path + "data/result/topics.txt").readlines()
	current = -1
	topic = []
	
	for line in lines:
		if line == "\n": 
			continue
		else:
			if line[0:3] == '	':
				topic[current].append(line[3:-1])	 
			else:
				current += 1
				topic.append([])
	return topic

def getwordIndex(dict, word):
	if not word in dict:
		index = len(dict)
		dict.append(word)
		return dict, index
	else:
		return dict, dict.index(word)

def addsSelections(request):
	response = ""
	topics = getTopics()
	fwords = open(path + 'data/testdata.dat','w')

	for p in Paragraph.objects.all():
		wordlist, r = textToCounts([], p.text)		
		counts = render_to_response('core/counts.html', {"counts": r}).content

		fwords.write(counts)	 
		fwords.close()

		command = path + "lda-c-dist/lda inf " + path + "lda-c-dist/settings.txt " + path + "data/result/final " + path + "data/words.dat " + path + "data/testresult"
		result = command
		try:
			pipe = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
			result += pipe
		except CalledProcessError as e:
			result += "\n" + str(e.returncode)
			result += "\n" + e.output
		pdata = open(path + "data/testresult-gamma.dat").readline()
		i = 0
		highest = (0, -1)
		response += str(p.id) + " "
		for weight in pdata.split():
			value = float(weight)
			if value > highest[0]:
				 highest = (value, i)
			i +=1
			if value > 1:
				response += str(value) + " "
		response += "\n" 
		
		if highest[1] != -1:
			source, created = Source.objects.get_or_create(name = algorithmname)

			t, created = Topic.objects.get_or_create(
				name = highest[1],
				source = source,
				description = ' '.join(topics[highest[1]]))
		
			s = Selection.objects.create(
				source = source,
				paragraph = p,
				startLetter = 0,
				endLetter = -1,
				user = None,
				topic = t,)
	return HttpResponse(response, 'text/plain')

def addSelections(request):
	fwords = open(path + 'data/testdata.dat','w')
	
	result = []
	for p in Paragraph.objects.all().order_by('id'):
		wordlist, r = textToCounts([], p.text)
		result.append(r)
		
	counts = render_to_response('core/counts.html', {"counts": result}).content
	fwords.write(counts)	 
	fwords.close()


	command = path + "lda-c-dist/lda inf " + path + "lda-c-dist/settings.txt " + path + "data/result/final " + path + "data/testdata.dat " + path + "data/testresult"
	result = command
	try:
			pipe = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
			result += pipe
	except CalledProcessError as e:
			result += "\n" + str(e.returncode)
			result += "\n" + e.output
	 

	response = ""
	weights = open(path + "data/testresult-gamma.dat").readlines()
	topics = getTopics()
	pnr = 0
	for p in Paragraph.objects.all().order_by('id'):
		pdata = weights[pnr]
		i = 0
		highest = 0
		highesti = -1
		response += str(p.id) + " "
		for weight in pdata.split():
			value = float(weight)
			if value > highest:
				 highesti = i
				 highest = value
			i +=1
			if value > 1:
				response += str(value) + " "
		response += "\n" 
		
		if highesti != -1:
			source, created = Source.objects.get_or_create(name = algorithmname)

			t, created = Topic.objects.get_or_create(
				name = highesti,
				source = source,
				description = ' '.join(topics[highesti]))
		
			s = Selection.objects.create(
				source = source,
				paragraph = p,
				startLetter = 0,
				endLetter = -1,
				user = None,
				topic = t,)
		pnr += 1
	return HttpResponse(response, 'text/plain')

def clear(request):
	Selection.objects.filter(source__name=algorithmname).delete()
	Topic.objects.filter(source__name=algorithmname).delete()
	return HttpResponse('done', 'text/plain')


def topics(request):
	topic = getTopics()
	message = ""
	i = 0
	for t in topic:
		message += "Topic " + str(i) + " "
		for word in t:
			message += word+ " "
		message += "\n"
		i += 1

	return HttpResponse(message, 'text/plain')
