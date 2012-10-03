from importdata.models import Partij, Hoofdstuk, Paragraaf, Programma
from django.contrib import admin

class ParagraphInline(admin.TabularInline):
	model = Paragraaf
	extra = 3

class SectionAdmin(admin.ModelAdmin):
	inlines = [ParagraphInline]
	list_filter = ['partij']




admin.site.register(Partij)
admin.site.register(Hoofdstuk, SectionAdmin)

admin.site.register(Paragraaf)
admin.site.register(Programma)