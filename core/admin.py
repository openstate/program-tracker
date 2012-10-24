from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from core.models import Paragraph, Section, Party, Program, SectionType


admin.site.register(Party)
admin.site.register(SectionType)


class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 3

class SectionAdmin(MPTTModelAdmin):
    inlines = [ParagraphInline]
    list_filter = ['program', 'program__party']
    list_display = ('name', 'program')
    
class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['party', 'date']
    list_display = ('name', 'party', 'date')


admin.site.register(Section, SectionAdmin)
admin.site.register(Program, ProgramAdmin)

