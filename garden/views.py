from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import *
from .mixins import UniversalMixins


class ChildrenListView(UniversalMixins, ListView):
    model = Children
    template_name = 'garden/childrens.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChildrenListView, self).add_childrens_with_parents(context=None, **kwargs)
        print(context)
        return context
