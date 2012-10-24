import re 

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson

from importdata.models import Partij
from importdata.utils import rreduce


def partij(request, pk):
    '''
        This is the most ugly method you will ever find, but since it is only for importing don't hold it against me :-)
        Part of the reformatting is done in the template and using a custom filter
    '''
    data = Partij.objects.get(pk = pk)
    content = render_to_response('importdata/partij_detail.html', {"partij": data}, mimetype="text/plain").content
    content = simplejson.loads(content)
    string = simplejson.dumps(content)
    string = re.sub(r', {}', r'', string, flags=re.S )
    string = re.sub(r', "sub": \[\]', r'', string, flags=re.S )
    string = re.sub(r'"head": "[\d\.\sIXV]+( |\.)', r'"head": "', string, flags=re.S ) #Strip numbers from head
    #string = re.sub(r'"sub": \[{"head": "", "sub": \[{"body": \[(.+?)\]}\]}\]', r'"body": [\1]', string, flags=re.S )
        
    content = simplejson.loads(string)
    
    rreduce(content)
    
    string = simplejson.dumps(content, indent=True, sort_keys=True)
    string = re.sub(r'\n\s+"",[ ]*', r'', string, flags=re.S )

    return HttpResponse(string, mimetype='text/plain')
