from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson

from core.models import Party, Program, Paragraph, SectionType, Section
from topic.models import Selection, Topic, Source

from core.api import PartyApi, ProgramApi, SectionTypeApi, SectionApi, ParagraphApi
from topic.api import SourceApi, TopicApi, SelectionApi


class JSONResponse(object):
    @classmethod
    def build(self, result, request):
        message = simplejson.dumps(result)
        mimetype = 'application/json'
        return HttpResponse(message, mimetype)


def home(request):
    message = "No XHR"
    mimetype = 'text/html'
    return HttpResponse(message, mimetype)

def parties(request):
    party_api = PartyApi()
    parties = party_api.serialize_parties()
    return JSONResponse.build(parties, request)

def programs(request):
    program_api = ProgramApi()
    programs = program_api.serialize_programs()
    return JSONResponse.build(programs, request)

def sections(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    section_api = SectionApi(program)
    sections = section_api.serialize_sections()
    return JSONResponse.build(sections, request)

def section_types(request):
    section_type_api = SectionTypeApi()
    section_types = section_type_api.serialize_section_types()
    return JSONResponse.build(section_types, request)

def sources(request):
    source_api = SourceApi()
    sources = source_api.serialize_sources()
    return JSONResponse.build(sources, request)

def topics(request):
    topic_api = TopicApi()
    topics = topic_api.serialize_topics()
    return JSONResponse.build(topics, request)

def selections(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    selection_api = SelectionApi(program)
    selections = selection_api.serialize_selections()
    return JSONResponse.build(selections, request)

def paragraph(request, paragraph_id):
    paragraph_obj = get_object_or_404(Paragraph, pk=paragraph_id)
    paragraph_api = ParagraphApi()
    paragraph = paragraph_api.serialize_paragraph(paragraph_obj)
    return JSONResponse.build(paragraph, request)

def section(request, section_id):
    section_obj = get_object_or_404(Section, pk=section_id)
    section_api = SectionApi(None) # FIXME: ugly hack, but works
    section = section_api.serialize_section(section_obj)
    return JSONResponse.build(section, request)

def program(request, program_id):
    program_obj = get_object_or_404(Program, pk=program_id)
    program_api = ProgramApi()
    program = program_api.serialize_program(program_obj)
    return JSONResponse.build(program, request)
