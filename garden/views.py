from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import *
from .mixins import UniversalMixins


class ChildrenListView(UniversalMixins, ListView):
    model = Children
    template_name = 'garden/childrens.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChildrenListView, self).add_childrens_with_parents(context=None, **kwargs)
        return context


class ChildDetail(DetailView):
    model = Children
    template_name = 'garden/child_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ChildDetail, self).get_context_data(**kwargs)
        context['child'] = self.get_object()
        context['parents'] = self.get_object().parent_set.all()
        return context