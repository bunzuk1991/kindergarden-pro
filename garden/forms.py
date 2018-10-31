from django.forms import ModelForm, DateInput, SelectDateWidget, TextInput, Textarea, FileInput, Select, Form, DateField
from django.forms.models import inlineformset_factory, modelformset_factory, BaseModelFormSet
from .models import *


class ChildForm(ModelForm):
    class Meta:
        model = Children
        fields = ['fullname', 'slug', 'date_of_birth', 'growth', 'image', 'weight', 'date_start', 'date_end', 'address', 'actual_group']
        widgets = {
            'date_of_birth': SelectDateWidget(),
            'image': FileInput()}

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-wrp'


ParentBaseFormSet = modelformset_factory(
    Parent,
    extra=0,
    fields=['fullname', 'date_of_birth', 'phone', 'relation', 'address', 'work', 'workplace'],
)


ParentFormSet = inlineformset_factory(
    Children,
    Parent,
    form=ChildForm,
    fields=['fullname', 'date_of_birth', 'phone', 'relation', 'address', 'work', 'workplace'],
    extra=0,
    formset=ParentBaseFormSet,
    can_delete=True,
    widgets={
        'fullname': TextInput(attrs={"readonly":True}),
        'phone': TextInput(attrs={"readonly":True}),
        'address': Textarea(attrs={"readonly":True}),
        'work': Textarea(attrs={"readonly":True, 'cols': None, 'rows': None}),
        'workplace': TextInput(attrs={"readonly":True}),
        'relation': Select(attrs={"disabled":True}),
        'date_of_birth': DateInput(attrs={"readonly":True})}
)