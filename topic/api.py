#!/usr/bin/python

import re
import datetime

from core.models import Party, Program, Section, SectionType, Paragraph

from .models import Source, Topic, Selection

from core.api import BaseApi, _encode_datetime


class SourceMixin(object):
    def serialize_source(self, source_obj):
        return {
            'id': source_obj.pk,
            'name': source_obj.name,
            'color': source_obj.color
        }


class TopicMixin(SourceMixin):
    def serialize_topic(self, topic_obj):
        return {
            'id': topic_obj.pk,
            'description': topic_obj.description,
            'created': _encode_datetime(topic_obj.creationdate),
            'source': self.serialize_source(topic_obj.source)
        }


class SelectionMixin(TopicMixin):
    def serialize_selection(self, selection_obj):
        if selection_obj.user is not None:
            username = selection_obj.user.username
        else:
            username = None

        return {
            'id': selection_obj.pk,
            'paragraph_id': selection_obj.paragraph_id,
            'source': self.serialize_source(selection_obj.source),
            'start': selection_obj.startLetter,
            'end': selection_obj.endLetter,
            'topic': self.serialize_topic(selection_obj.topic),
            'user': username,
            'created': _encode_datetime(selection_obj.creationdate)
        }


class SourceApi(BaseApi, SourceMixin):
    def serialize_sources(self):
        source_objs = Source.objects.order_by('name').all()
        sources = []
        
        for source_obj in source_objs:
            sources.append(self.serialize_source(source_obj))
        
        return sources


class TopicApi(BaseApi, TopicMixin):
    def serialize_topics(self):
        topic_objs = Topic.objects.order_by('name').all()
        topics = []
        
        for topic_obj in topic_objs:
            topics.append(self.serialize_topic(topic_obj))
        
        return topics

class SelectionApi(BaseApi, SelectionMixin):
    program = None

    def __init__(self, program):
        self.program = program
    
    def serialize_selections(self):
        selection_objs = Selection.objects.filter(
            paragraph__section__program_id=self.program.pk
        ).select_related().all()
        selections = []
        
        for selection_obj in selection_objs:
            selections.append(self.serialize_selection(selection_obj))
        
        return selections
