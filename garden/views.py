from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView
from .models import *
from .forms import *
from .mixins import UniversalMixins
from .custom import *


class ChildrenListView(UniversalMixins, ListView):
    model = Children
    template_name = 'garden/childrens.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChildrenListView, self).add_childrens_with_parents(context=None, **kwargs)
        return context


# class ChildDetail(DetailView):
#     model = Children
#     template_name = 'garden/child_detail.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ChildDetail, self).get_context_data(**kwargs)
#         context['child'] = self.get_object()
#         context['parents'] = self.get_object().parent_set.all()
#         return context


class ChildDetailView(View):
    template_name = 'garden/child_detail.html'
    model = None
    context = {}

    def get(self, request, *args, **kwargs):
        json_query = False
        json_def = ''

        # перевірка на наявність в GET мітки json
        if 'json_query' in self.request.GET:
            json_query = True
            json_def = self.request.GET.get('json_def')

        if not json_query:
            child_slug = kwargs['slug']
            child_obj = get_object_or_404(Children, slug = child_slug)

            formset = ParentFormSet(queryset=child_obj.parent_set.all(), prefix='parent')
            self.context['form'] = ChildForm(request.POST or None, instance=child_obj, prefix='child')
            self.context['formset'] = formset
            self.context['slug'] = child_obj.slug

            return render(self.request, self.template_name, self.context)
        else:
            if json_def == 'relations':
                list_json = get_relation_list()
                return list_json
            else:
                return Http404


# test for inlines forms
class ChildCreateView(View):
    template_name = 'garden/child-create.html'
    context = {}

    def get(self, request, *args, **kwargs):
        formset = ParentFormSet(queryset=Parent.objects.none())
        self.context['form'] = ChildForm(request.POST or None)
        self.context['formset'] = formset

        return render(self.request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = ChildForm(request.POST or None)
        formset = ParentFormSet(request.POST or None, queryset=Parent.objects.none())

        if form.is_valid() and formset.is_valid():
            child_new = form.save(commit=False)

            for key in form.fields:
                setattr(child_new, key, form.cleaned_data[key])
            child_new.save()

            parents = formset.save(commit=False)
            current_idx = -1
            for parent in parents:
                current_idx += 1
                act_form = formset[current_idx]
                for key in act_form.fields:
                    setattr(parent, key, act_form.cleaned_data[key])
                parent.child = child_new
                parent.save()

            return HttpResponseRedirect(reverse('childrens-list'))

        self.context['form'] = form
        self.context['formset'] = formset
        return render(self.request, self.template_name, self.context)
