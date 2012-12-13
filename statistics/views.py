from datetime import date

from chartit import PivotDataPool, PivotChart


from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404


from core.models import Program, Party
from topic.models import Topic, Source
from topic.models import Selection
from core.models import Paragraph
from statistics.models import ProgramStat

def sourceindex(request, source):
    source = get_object_or_404(Source, pk=source)

    years = Program.objects.all().filter(stats__topic__source=source).values('date').distinct()
    parties = Party.objects.all()
    topics = Topic.objects.all().filter(source=source).exclude(stats__isnull=True).order_by('name')
    return render_to_response('statistics/index.html', {'parties': parties, 'topics': topics, 'years': years, 'source': source})


def calc(request, source):
    ProgramStat.objects.filter(topic__source__pk=source).delete()
    def do_work():
        for p in Program.objects.all().annotate(
                        selection_count = Count('sections__paragraphs__selections')).annotate(
                        paragraph_count = Count('sections__paragraphs')):
            topics = Topic.objects.filter(selections__paragraph__section__program=p, source__pk=source).distinct().annotate(paragraph_count = Count('selections__paragraph'))
            topic_count = topics.count()
            program_word_count_paragraphs = sum(map(lambda x: len(x.text.split(' ')), Paragraph.objects.filter(section__program=p).distinct()))
            program_word_count_selections = sum(map(lambda x: len(x.text.split(' ')), Paragraph.objects.filter(section__program=p, selections__isnull=False).distinct()))
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
                        program_word_count_selections=program_word_count_selections,
                        program_word_count_paragraphs=program_word_count_paragraphs,
                        word_nm = float(word_count) / float(program_word_count_selections),
                        paragraph_nm = float(count) / float(p.paragraph_count),
                        selection_nm = float(count) / float(p.selection_count),
                        ).save()

                yield "%s (%s) %s count: %s word_count:%s topic_count:%s paragraph_count:%s selection_count:%s topic_paragraph_count:%s \n" % ( p.name, p.party.name, t.name, count, word_count, topic_count, p.paragraph_count, p.selection_count, t.paragraph_count)
                 

    
    return HttpResponse(do_work(), mimetype='text/plain')

def party(request, source, pk):
    party = get_object_or_404(Party, pk=pk)
    source = get_object_or_404(Source, pk=source)

    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    pivotdata = \
        PivotDataPool(
           series =
            [{'options': {
               'source': ProgramStat.objects.filter(program__party=party, topic__source=source),
               'categories': ['program__date'],
               'legend_by': 'topic__name'
               },
              'terms': {
                'count': {'func':Sum('count'), 'legend_by': 'topic__name', },
                'word': {'func':Sum('word_nm'), 'legend_by': 'topic__name', },
                'paragraph': {'func':Sum('paragraph_nm'), 'legend_by': 'topic__name', },
                'selection': {'func':Sum('word_nm'), 'legend_by': 'topic__name', },
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
                   'text': 'Aandacht per jaar voor partij: ' + unicode(party)},
               'xAxis': {
                    'title': {
                       'text': 'Programma'}},
                'yAxis': {
                    'title': {
                       'text': 'Aandacht'}}})

    #Step 3: Send the PivotChart object to the template.
    return render_to_response('chartit.html', {'rainpivchart': pivot})

def year(request, source, pk):

    source = get_object_or_404(Source, pk=source)

    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    pivotdata = \
        PivotDataPool(
           series =
            [{'options': {
               'source': ProgramStat.objects.filter(program__date__year=pk, topic__source=source),
               'categories': ['program__party__name'],
               'legend_by': 'topic__name'
               },
              'terms': {
                'count': {'func':Sum('count'), 'legend_by': 'topic__name', },
                'word': {'func':Sum('word_nm'), 'legend_by': 'topic__name', 'top_n_per_cat': 3},
                'paragraph': {'func':Sum('paragraph_nm'), 'legend_by': 'topic__name', },
                'selection': {'func':Sum('selection_nm'), 'legend_by': 'topic__name'},
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
                   'text': 'Aandacht per partij voor jaar: ' + pk},
               'xAxis': {
                    'title': {
                       'text': 'Partij'}},
                'yAxis': {
                    'title': {
                       'text': 'Aandacht'}}})

    #Step 3: Send the PivotChart object to the template.
    return render_to_response('chartit.html', {'rainpivchart': pivot})

def topic(request, source, pk):
    topic = get_object_or_404(Topic, pk=pk)
    source = get_object_or_404(Source, pk=source)

    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    pivotdata = \
        PivotDataPool(
           series =
            [{'options': {
               'source': ProgramStat.objects.filter(topic=topic, topic__source=source),
               'categories': ['program__party__name', 'program__date'],
               },
              'terms': {
                'count': {'func':Sum('count'), },
                'word': {'func':Sum('word_nm'), },
                'paragraph': {'func':Sum('paragraph_nm'), },
                'selection': {'func':Sum('selection_nm'), },
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
                   'text': 'Aandacht per topic per partij per jaar: ' + unicode(topic)},
               'xAxis': {
                    'title': {
                       'text': 'Partij'}},
                'yAxis': {
                    'title': {
                       'text': 'Aandacht'}}})

    #Step 3: Send the PivotChart object to the template.
    return render_to_response('chartit.html', {'rainpivchart': pivot})