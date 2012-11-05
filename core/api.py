#!/usr/bin/python

import re
import datetime

from .models import Party, Program, Section, SectionType, Paragraph

def _encode_datetime(obj):
    # FIXME: what about timezones?
	if isinstance(obj, datetime.date):
		return obj.strftime('%Y-%m-%dT00:00:00Z')
	if isinstance(obj, datetime.datetime):
		return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
	raise TypeError(repr(obj) + " is not JSON serializable")


class BaseApi(object):
    pass


class PartyMixin(object):
    def serialize_party(self, party_obj):
        return {
            'id': party_obj.pk,
            'name': party_obj.full_name,
            'short_name': party_obj.name,
            'pm_id': party_obj.pm_id
        }


class ProgramMixin(PartyMixin):
    def serialize_program(self, program_obj):
        return {
            'id': program_obj.pk,
            'name': program_obj.name,
            'date': _encode_datetime(program_obj.date),
            'party': self.serialize_party(program_obj.party)
        }


class SectionTypeMixin(object):
    def serialize_sectiontype(self, sectiontype_obj):
        return {
            'id': sectiontype_obj.pk,
            'name': sectiontype_obj.name
        }


class SectionMixin(ProgramMixin, SectionTypeMixin):
    def serialize_section(self, section_obj):
        if section_obj.program is not None:
            program_serialized = self.serialize_program(section_obj.program)
        else:
            program_serialized = None

        return {
            'id': section_obj.pk,
            'type': self.serialize_sectiontype(section_obj.type),
            'program': program_serialized,
            # FIXME: sections and subsections
            'order': section_obj.order
        }


class PartyApi(BaseApi, PartyMixin):
    def serialize_parties(self):
        party_objs = Party.objects.order_by('name').all()
        parties = []

        for party_obj in party_objs:
            parties.append(self.serialize_party(party_obj))

        return parties

class ProgramApi(BaseApi, ProgramMixin):
    def serialize_programs(self):
        program_objs = Program.objects.order_by('-date').select_related().all()
        programs = []
        
        for program_obj in program_objs:
            programs.append(self.serialize_program(program_obj))
        
        return programs
