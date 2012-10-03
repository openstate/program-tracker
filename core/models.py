from django.db import models

# Create your models here.
class Party(models.Model):
	name = models.CharField(max_length=200)
	
	class Meta:
		verbose_name_plural = "parties"

	def __unicode__(self):
		return self.name

class Program(models.Model):
	date = models.DateField()
	party = models.ForeignKey(Party, related_name='programs')
	name = models.CharField(max_length=200, default='')
	section = models.OneToOneField('core.Section', related_name='program_root', null=True, on_delete=models.SET_NULL)
	
	class Meta:
		get_latest_by = "date"

	def __unicode__(self):
		return u'%s (%s %s)' % (self.name, self.party, self.date)
		
	@models.permalink
	def get_absolute_url(self):
		return ('program_view', [str(self.id)])

class SectionType(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Section(models.Model):
	name = models.CharField(max_length=200)
	program = models.ForeignKey(Program, blank=True, null=True, related_name='sections')
	parent = models.ForeignKey('self', blank=True, null=True, related_name='subsections')
	type = models.ForeignKey(SectionType, default=1)
	order = models.IntegerField(default=0)
	
	class Meta:
		ordering = ['order']

	def __unicode__(self):
		return u'Sectie %s uit %s' % (self.name, self.program)

	
	@property
	def text(self):
		return self.name + "\n" + "\n\n".join(p.text for p in self.paragraphs.all().order_by('order'))
		
	def save(self, *args, **kwargs):
		# Only modify number if creating for the first time (is default 0)
		if self.order == 0:
			# Grab the highest current index (if it exists)
			try:
				recent = Section.objects.filter(parent__exact=self.parent).order_by('-order')[0]
				self.order = recent.order + 1
			except IndexError:
				self.order = 1
		# Call the "real" save() method
		super(Section, self).save(*args, **kwargs)



class Paragraph(models.Model):
	text = models.TextField()
	section = models.ForeignKey(Section, related_name='paragraphs')
	order = models.IntegerField(default=0)
	class Meta:
		ordering = ['order']


	def __unicode__(self):
		return u'Paragraaf %s uit %s' % (self.order, self.section)

	def save(self, *args, **kwargs):
		# Only modify number if creating for the first time (is default 0)
		if self.order == 0:
			# Grab the highest current index (if it exists)
			try:
				recent = Paragraph.objects.filter(section__exact=self.section).order_by('-order')[0]
				self.order = recent.order + 1
			except IndexError:
				self.order = 1
		# Call the "real" save() method
		super(Paragraph, self).save(*args, **kwargs)

