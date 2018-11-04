from django.forms import ModelForm, DateInput, SelectDateWidget, TextInput, Textarea, FileInput, Select, Form, DateField, ClearableFileInput, ValidationError, CharField
from django.forms.models import inlineformset_factory, modelformset_factory, BaseModelFormSet
from .models import *


class ChildForm(ModelForm):
    class Meta:
        model = Children
        fields = ['fullname', 'slug', 'date_of_birth', 'growth', 'image', 'weight', 'date_start', 'date_end', 'address', 'actual_group']
        widgets = {
            'date_of_birth': SelectDateWidget()}
            # 'image': FileInput()}

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-wrp'
            if visible.name == 'relation':
                visible.field.widget.attrs['class'] = 'disabled-text-area'


class BaseParentFormSet(BaseModelFormSet):
    address = CharField(max_length=250, required=False, empty_value='')

    class Meta:
        model = Parent
        fields = ['fullname', 'date_of_birth', 'phone', 'relation', 'address', 'work', 'workplace']
        # exclude = ['id']


ParentFormSet = inlineformset_factory(
    Children,
    Parent,
    form=ChildForm,
    fields=['fullname', 'date_of_birth', 'phone', 'relation', 'address', 'work', 'workplace'],
    extra=0,
    formset=BaseParentFormSet,
    can_delete=True,
    widgets={
        'fullname': TextInput(attrs={"readonly":True}),
        'phone': TextInput(attrs={"readonly":True}),
        'address': Textarea(attrs={"readonly":True, 'required':False}),
        'work': Textarea(attrs={"readonly":True, 'cols': None, 'rows': None}),
        'workplace': TextInput(attrs={"readonly":True}),
        'relation': Select(),
        'date_of_birth': DateInput(attrs={"readonly":True})},
    localized_fields=['date_of_birth']
)