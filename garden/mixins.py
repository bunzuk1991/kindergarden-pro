from .models import *
from django.views.generic.list import MultipleObjectMixin


class UniversalMixins(object):

    def add_childrens_with_parents(self, *,  context=None, **kwargs):
        children_list = []

        for child in Children.objects.all():
            child_element = {}
            child_element['child'] = child
            child_element['parents'] = Parent.objects.filter(child=child)
            children_list.append(child_element)

        if context == None:
            context = {'children_with_parents': children_list}
        else:
            context['children_with_parents'] = children_list

        return context