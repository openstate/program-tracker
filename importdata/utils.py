import sys
import os
import re
from xml.dom.minidom import parse

from django.conf import settings
from django.utils import simplejson

from core.models import Program, Section, SectionType, Party, Paragraph
from topic.models import Source, Topic, Selection

def rreduce(node):

    if 'sub' in node:
        for sub in node['sub']:
            rreduce(sub)
    
        sub = node['sub'][0]
        if not 'body' in node and (not 'head' in sub or sub['head'].strip() == ''):
            if 'sub' in sub:
                if len(node['sub']) != 1:
                    sub['sub'].extend(node['sub'][1:])
                node['sub'] = sub['sub']
            else:
                del node['sub']

            if 'body' in sub:
                node['body'] = sub['body']

def import_json_program(file, party, date):

    json_data=open(settings.PROJECT_DIR("programmas") + '/%s.json' % file)
    data = simplejson.load(json_data)
    json_data.close()

    program, was_created = Program.objects.get_or_create(
        date=date,
        party=party,
        name=data['head'],
    )
    
    #delete old sections and paragraphs
    Section.objects.filter(program__isnull=True).delete()
    Section.objects.filter(program = program).delete()
    
    s = Section.objects.create(name=data['head'], program=program)
    program.section = s
    program.save()
    

    
    if "body" in data:
         for p in data['body']:
             s.paragraphs.create(text=p)
    
    si = 1
    if "sub" in data:
         for subdata in data['sub']:
              addsection(s, subdata, si, program)
              si = si + 1
    
    s.save()

def addsection(section, data, si, program):
    if "type" in data:
        section_type, was_created = SectionType.objects.get_or_create(name=data['type'])
    else:
        section_type = SectionType.objects.get(name="tekst")

    s = Section(name=data['head'], parent=section, type=section_type, order=si, program=program)
    s.save()

    i = 1
    if "body" in data:
         for p in data['body']:
             Paragraph(text=p, section_id=s.id, order=i).save()
             i = i + 1

    si = 1
    if "sub" in data:    
         for subdata in data['sub']:
              addsection(s, subdata, si, program)
              si = si + 1


def import_lipschits(year):
    #delete old
    Program.objects.filter(date = '%s-01-01' % year).delete()
    Section.objects.filter(program__date = '%s-01-01' % year).delete()

    xml = parse(settings.PROJECT_DIR("LipschitsBooksinXML") + '/VP_%s.party-topicnr-content.xml' % year)
    chapters = xml.getElementsByTagName("chapter")
    for chapter in chapters:        
        pm_id = chapter.getAttributeNode('party').value
        party, created = Party.objects.get_or_create(pm_id=pm_id, defaults={"full_name": pm_id, "name": pm_id})
        program = Program(party=party, name = "Programma %s" % year, date = ('%s-01-01' % year))
        type = SectionType.objects.get(name="tekst")
        program.save()
        s = Section.objects.create(name = "Programma %s" % year, type=type, order=1, program=program)
        program.section = s
        program.save()
        
        for p in chapter.getElementsByTagName("p"):
            text = " ".join(t.nodeValue for t in p.childNodes if t.nodeType == t.TEXT_NODE)
            text = process_text(text)
            
            paragraph = s.paragraphs.create(text=text)
            
            for theme in p.getElementsByTagName('theme'):
                name = theme.getAttributeNode('id').value
                name = name.replace('_',' ')

                source, created = Source.objects.get_or_create(name = 'lipschits')

                t, created = Topic.objects.get_or_create(
                    name = name,
                    source = source)
            
                Selection.objects.create(
                    source = source,
                    paragraph = paragraph,
                    startLetter = 0,
                    endLetter = -1,
                    user = None,
                    topic = t,)

  
def process_text(text):
    text = re.sub(r'^\d+ ', '', text)
    text = re.sub(r'\u2022$\s*', '', text)
    return text
