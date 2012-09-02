from core.models import Paragraph, Section, Party, Program, SectionType
from django.contrib import admin

admin.site.register(Party)
admin.site.register(SectionType)


class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 3

class SectionAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]
    list_filter = ['program', 'parent']
    list_display = ('name', 'parent', 'programf', 'order')
    list_editable = ['order']
    
class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['party', 'date']
    list_display = ('name', 'party', 'date')


admin.site.register(Section, SectionAdmin)
admin.site.register(Program, ProgramAdmin)

