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
        return {
            'id': selection_obj.pk,
            'paragraph_id': selection_obj.paragraph_id,
            'source': self.serialize_source(selection_obj.source),
            'start': selection_obj.startLetter,
            'end': selection_obj.endLetter,
            'topic': self.serialize_topic(selection_obj.topic),
            'user': selection_obj.user.username,
            'created': _encode_datetime(selection_obj.creationdate)
        }
