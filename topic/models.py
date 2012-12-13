from django.db import models

# Create your models here.
class Source(models.Model):
	name = models.CharField(max_length=200)
	color = models.CharField(max_length=20, default="#ffccff")
	
	def __unicode__(self):
		return u'%s' % (self.name)

class Thesaurus(Source):
	pass


class Topic(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	creationdate = models.DateField(auto_now_add=True);
	source = models.ForeignKey(Source, related_name='topics', blank=True, null=True)
	thesaurus = models.ForeignKey(Thesaurus, related_name='ttopics', blank=True, null=True)

	
	def __unicode__(self):
		return u'%s' % (self.name)
		
	@models.permalink
	def get_absolute_url(self):
		return ('topic_view', [str(self.id)])	

class Selection(models.Model):
	paragraph = models.ForeignKey('core.Paragraph', related_name='selections')
	source = models.ForeignKey(Source, related_name='selections', blank=True, null=True)
	startLetter = models.IntegerField(default=0)
	endLetter = models.IntegerField(default=-1)
	topic = models.ForeignKey(Topic, related_name='selections')
	user = models.ForeignKey('auth.User', blank=True, null=True)
	creationdate = models.DateField(auto_now_add=True);
	extra = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return u'%s: ((%s) van %s tot %s)' % (self.topic, self.paragraph, self.startLetter, self.endLetter)
		
	def prefix(self):
		return self.paragraph.text[:self.startLetter]
		
	def text(self):
		if self.endLetter < 0:
			return self.paragraph.text
		else:
			return self.paragraph.text[self.startLetter:self.endLetter]
		
	def postfix(self):
		if self.endLetter < 0:
			return ''
		else:
			return self.paragraph.text[self.endLetter:]
