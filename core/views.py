from django.template import Context, loader
from core.models import Party
from core.models import Section
from core.models import Paragraph
from core.models import Program
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

# Create your views here.
def index(request):
    parties = Program.objects.all().order_by('-party')[:5]
    c = {
        'parties': parties,
    }
    return render_to_response('core/index.html', c)


def program(request, program_id):    
    program = get_object_or_404(Program, pk=program_id)

    c = {
        'program': program,
    }
    return render_to_response('core/program.html', c)
