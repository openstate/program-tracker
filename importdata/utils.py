import sys
import os
import re

from django.conf import settings
from django.utils import simplejson

from core.models import Program, Section, SectionType, Party, Paragraph

def rreduce(node):

    if 'sub' in node:
        for sub in node['sub']:
            rreduce(sub)
    
        sub = node['sub'][0]
        if not 'body' in node and len(node['sub']) == 1 and (not 'head' in sub or sub['head'].strip() == ''):
            if 'sub' in sub:
                node['sub'] = sub['sub']
            else:
                del node['sub']
            if 'body' in sub:
                node['body'] = sub['body']
        elif not 'body' in node and (not 'head' in sub or sub['head'].strip() == ''):
            if 'sub' in sub:
                sub['sub'].extend(node['sub'][1:])
                node['sub'] = sub['sub']
            else:
                del node['sub']
            if 'body' in sub:
                node['body'] = sub['body']

def import_json_program(file, program_id):
    #delete old sections and paragraphs
    program = Program.objects.get(pk=program_id)
    Section.objects.filter(program__isnull=True).delete()
    Section.objects.filter(program = program).delete()

    json_data=open(settings.PROJECT_DIR("programmas") + '/%s.json' % file)
    data = simplejson.load(json_data)
    json_data.close()
    
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

    s = Section(name=data['head'], type=section_type, order=si, program=program)
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

    section.subsections.add(s)
