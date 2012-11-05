#!/usr/bin/python

import re

from .models import Party, Program, Section, SectionType, Paragraph

class BaseApi(object):
    pass


class PartyApi(BaseApi):
    def serialize_parties(self):
        party_objs = Party.objects.order_by('name').all()
        parties = []

        for party_obj in party_objs:
            parties.append({
                'name': party_obj.full_name,
                'short_name': party_obj.name,
                'pm_id': party_obj.pm_id
            })

        return parties
