from django.template.defaulttags import register
from django import template
#collectstatic yapmayı unutma
register = template.Library()
@register.filter

def index(List, i):

    return List[int(i)]


'''
def get_item(dictionary, key):
    return dictionary.get(key)
'''