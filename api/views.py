from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson

from core.models import Party, Program, Paragraph, SectionType, Section
from topic.models import Selection, Topic, Source

from core.api import PartyApi, ProgramApi


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


    