import re 
from django.utils.safestring import mark_safe
from django import template
register = template.Library()
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import NavigableString
from django.utils import simplejson


@register.filter
def replace(string, args): 
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub( search, replace, string )
  
def replacements(var):
    return {
        "p": lambda x: x
    }[var]
  

  
@register.filter  
def fix(string):
    string = re.sub(r'<br />[\r\n]{1,2}', r"\\n", string, flags=re.S )
    string = re.sub(r'<p><i>(.+?)</i></p>', r'\1', string, flags=re.S )
    string = re.sub(r'<i>(.+?)</i>', r'*\1*', string, flags=re.S )
    string = re.sub(r'<em>(.+?)</em>', r'*\1*', string, flags=re.S )
    string = re.sub(r'<b>(.+?)</b>', r'**\1**', string, flags=re.S )
    string = re.sub(r'<p>(.+?)</p>', r'\1', string, flags=re.S )
    string = re.sub(r'<p></p>', r'', string, flags=re.S )
    string = re.sub(r'<span>', r'', string, flags=re.S )
    string = re.sub(r'</span>', r'', string, flags=re.S )
    string = re.sub(r'<sub>2</sub>', r'2', string, flags=re.S )
    string = re.sub(r'<a href=\"([^"]+)\"([^>]+)>([^<]+)</a>', r'[\3](\1)', string, flags=re.S )

    soup = BeautifulSoup(string,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    
    currenth3sub = []
    currenth4sub = []
    sub = []
    currentbody = []
    result = {'body': currentbody, 'sub': sub}
    
    for element in soup:
        currenth3sub, currenth4sub, currentbody = parse_element(element, sub, currenth3sub, currenth4sub, currentbody)
        
    return mark_safe(simplejson.dumps(result))

def parse_element(element, sub, currenth3sub, currenth4sub, currentbody):
    if isinstance(element, NavigableString):
        appendString(element, currentbody)
    elif element.name == 'h3':
        currentbody = []
        currenth3sub = []
        sub.append({'head': element.string, 'body': currentbody, 'sub': currenth3sub})
    elif element.name == 'h4':
        currentbody = []
        currenth4sub = []
        currenth3sub.append({'head': element.string, 'body': currentbody, 'sub': currenth4sub})
    elif element.name == 'ul' or element.name == 'ol':
        for li in element.contents:
            appendString(unicode(li)[4:-5], currentbody)
    else:
        #should not be needed
        appendString(element, currentbody)
        
    return currenth3sub, currenth4sub, currentbody
        
def appendString(element, clist):
    string = unicode(element).strip()
    if string != '':
        for string in re.split(r'\\n|[\n]', string):
            clist.append(string.strip())

