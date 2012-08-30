from core.models import Paragraph, Section, Party, Program, SectionType
from django.contrib import admin

admin.site.register(Party)
admin.site.register(SectionType)


class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 3

class SectionAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]
    list_filter = ['program']
    list_display = ('program', 'name')
    
class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['party', 'date']
    list_display = ('name', 'party', 'date')


admin.site.register(Section, SectionAdmin)
admin.site.register(Program, ProgramAdmin)

