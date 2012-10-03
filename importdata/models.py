from django.db import models

# Create your models here.

class Partij(models.Model):
	partij = models.CharField(max_length=765)
	korte_naam = models.CharField(max_length=765)
	titel = models.CharField(max_length=765)

	def __unicode__(self):
		return self.partij
	
	class Meta:
		db_table = u'partijen'

class Hoofdstuk(models.Model):
	partij = models.ForeignKey(Partij, related_name='chapters')
	hoofdstuk = models.CharField(max_length=765)
	volgorde = models.IntegerField()
	
	def __unicode__(self):
		return self.hoofdstuk
		
	class Meta:
		db_table = u'hoofdstukken'

class Paragraaf(models.Model):
	partij = models.ForeignKey(Partij, related_name='paragraphs')
	hoofdstuk = models.ForeignKey(Hoofdstuk, related_name='paragraphs')
	kop = models.CharField(max_length=765)
	tekst = models.TextField()
	volgorde = models.IntegerField()
	
	def __unicode__(self):
		return self.kop
	
	class Meta:
		db_table = u'paragrafen'

class Programma(models.Model):
	partij = models.CharField(max_length=765)
	titel = models.CharField(max_length=765)
	hoofdstuk = models.CharField(max_length=765)
	paragraaf_kop = models.CharField(max_length=765)
	tekst = models.TextField()
	volgorde = models.IntegerField()
	naam_kort = models.CharField(max_length=765)
	jaar = models.IntegerField()
	class Meta:
		db_table = u'programmas_utf8'
