from django.db import models

# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Program(models.Model):
    date = models.DateField()
    party = models.ForeignKey(Party, related_name='programs')
    name = models.CharField(max_length=200, default='')

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

    def __unicode__(self):
        return u'Sectie %s uit %s' % (self.name, self.program)


class Paragraph(models.Model):
    text = models.TextField()
    section = models.ForeignKey(Section, related_name='paragraphs')
    number = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Paragraaf %s uit %s' % (self.number, self.section)

    def save(self, force_insert=False, force_update=False):
        # Only modify number if creating for the first time (is default 0)
        if self.number == 0:
            # Grab the highest current index (if it exists)
            try:
                recent = Paragraph.objects.filter(section__exact=self.section).order_by('-number')[0]
                self.number = recent.number + 1
            except IndexError:
                self.number = 1
        # Call the "real" save() method
        super(Paragraph, self).save(force_insert, force_update)

