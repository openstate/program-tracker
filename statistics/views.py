from datetime import date

from chartit import PivotDataPool, PivotChart


from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import simplejson
from django.shortcuts import render_to_response


from core.models import Program, Party
from topic.models import Topic
from topic.models import Selection
from core.models import Paragraph
from statistics.models import ProgramStat


def index(request):
    years = Program.objects.all().exclude(stats__isnull=True).values('date').distinct()
    parties = Party.objects.all()
    topics = Topic.objects.all().exclude(stats__isnull=True)
    return render_to_response('statistics/index.html', {'parties': parties, 'topics': topics, 'years': years})


def calc(request):
    def do_work():
        for p in Program.objects.all().annotate(
                        selection_count = Count('sections__paragraphs__selections')).annotate(
                        paragraph_count = Count('sections__paragraphs')):
            topics = Topic.objects.filter(selections__paragraph__section__program=p).distinct().annotate(paragraph_count = Count('selections__paragraph'))
            topic_count = topics.count()
            program_word_count = sum(map(lambda x: len(x.text.split(' ')), Paragraph.objects.filter(section__program=p).distinct()))
            for t in topics:  
                paragraphs = Paragraph.objects.filter(section__program=p, selections__topic=t).distinct()
                word_count = sum(map(lambda x: len(x.text.split(' ')), paragraphs))
                count = len(paragraphs)

                if count > 0:
                    ProgramStat(
                        program=p, 
                        topic = t, 
                        count = count, 
                        word_count=word_count, 
                        topic_count=topic_count, 
                        selection_count=p.selection_count, 
                        paragraph_count=p.paragraph_count, 
                        topic_paragraph_count=t.paragraph_count, 
                        program_word_count=program_word_count,
                        word_nm = float(word_count) / float(program_word_count),
                        paragraph_nm = float(count) / float(p.paragraph_count),
                        selection_nm = float(count) / float(p.selection_count),
                        ).save()

                yield "%s (%s) %s count: %s word_count:%s topic_count:%s paragraph_count:%s selection_count:%s topic_paragraph_count:%s \n" % ( p.name, p.party.name, t.name, count, word_count, topic_count, p.paragraph_count, p.selection_count, t.paragraph_count)
                 

    
    return HttpResponse(do_work(), mimetype='text/plain')

def party(request, pk):
    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    pivotdata = \
        PivotDataPool(
           series =
            [{'options': {
               'source': ProgramStat.objects.filter(program__party_id=pk),
               'categories': ['program__date'],
               'legend_by': 'topic__name'
               },
              'terms': {
                'count': {'func':Sum('count'), 'legend_by': 'topic__name', },
                'word': {'func':Sum('word_nm'), 'legend_by': 'topic__name', },
                'paragraph': {'func':Sum('paragraph_nm'), 'legend_by': 'topic__name', },
                'selection': {'func':Sum('selection_nm'), 'legend_by': 'topic__name', },
                }
                }
             ],
           )

    #Step 2: Create the PivotChart object
    pivot = \
        PivotChart(
            datasource = pivotdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': True},
                'terms':[
                 'selection']}],
            chart_options =
              {
              'chart': {
                'height': 3000,
                'width': 1000,

              },
              'title': {
                   'text': 'Aandacht per jaar voor partij:'},
               'xAxis': {
                    'title': {
                       'text': 'Programma'}},
                'yAxis': {
                    'title': {
                       'text': 'Aandacht'}}})

    #Step 3: Send the PivotChart object to the template.
    return render_to_response('chartit.html', {'rainpivchart': pivot})

def year(request, pk):
    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    pivotdata = \
        PivotDataPool(
           series =
            [{'options': {
               'source': ProgramStat.objects.filter(program__date__year=pk),
               'categories': ['program__party__name'],
               'legend_by': 'topic__name'
               },
              'terms': {
                'count': {'func':Sum('count'), 'legend_by': 'topic__name', },
                'word': {'func':Sum('word_nm'), 'legend_by': 'topic__name', 'top_n_per_cat': 3},
                'paragraph': {'func':Sum('paragraph_nm'), 'legend_by': 'topic__name', },
                'selection': {'func':Sum('selection_nm'), 'legend_by': 'topic__name', 'top_n_per_cat': 3},
                }
                }
             ],
           )

    #Step 2: Create the PivotChart object
    pivot = \
        PivotChart(
            datasource = pivotdata,
            series_options =
              [{'options':{
                  'type': 'bar',
                  'stacking': False},
                'terms':[
                 'word']}],
            chart_options =
              {
              'chart': {
                'height': 3000,
                'width': 1000,

              },
              'title': {
                   'text': 'Aandacht per jaar voor partij:'},
               'xAxis': {
                    'title': {
                       'text': 'Partij'}},
                'yAxis': {
                    'title': {
                       'text': 'Aandacht'}}})

    #Step 3: Send the PivotChart object to the template.
    return render_to_response('chartit.html', {'rainpivchart': pivot})

def topic(request, pk):
    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    pivotdata = \
        PivotDataPool(
           series =
            [{'options': {
               'source': ProgramStat.objects.filter(topic=pk),
               'categories': ['program__party__name', 'program__date'],
               },
              'terms': {
                'count': {'func':Sum('count'), 'legend_by': 'topic__name', },
                'word': {'func':Sum('word_nm'), 'legend_by': 'topic__name', },
                'paragraph': {'func':Sum('paragraph_nm'), 'legend_by': 'topic__name', },
                'selection': {'func':Sum('selection_nm'), 'legend_by': 'topic__name', },
                }
                }
             ],
           )

    #Step 2: Create the PivotChart object
    pivot = \
        PivotChart(
            datasource = pivotdata,
            series_options =
              [{'options':{
                  'type': 'bar',
                  'stacking': False},
                'terms':[
                 'selection']}],
            chart_options =
              {
              'chart': {
                'height': 3000,
                'width': 1000,

              },
              'title': {
                   'text': 'Aandacht per jaar voor partij:'},
               'xAxis': {
                    'title': {
                       'text': 'Partij'}},
                'yAxis': {
                    'title': {
                       'text': 'Aandacht'}}})

    #Step 3: Send the PivotChart object to the template.
    return render_to_response('chartit.html', {'rainpivchart': pivot})