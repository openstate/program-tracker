from django.db import models

from core.models import Program
from topic.models import Topic

# Create your models here.


class ProgramStat(models.Model):
	program = models.ForeignKey(Program, related_name='stats')
	topic = models.ForeignKey(Topic, related_name='stats')
	count = models.PositiveIntegerField()
	word_count = models.PositiveIntegerField()
	topic_count = models.PositiveIntegerField()
	paragraph_count = models.PositiveIntegerField()
	selection_count = models.PositiveIntegerField()
	topic_paragraph_count = models.PositiveIntegerField()
	program_word_count = models.PositiveIntegerField()
	word_nm = models.FloatField()
	paragraph_nm = models.FloatField()
	selection_nm = models.FloatField()

	def __unicode__(self):
		return '%s %s %s' % (self.count, self.program, self.topic)
