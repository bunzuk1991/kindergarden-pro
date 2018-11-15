from django.forms import ModelForm, DateInput, SelectDateWidget, TextInput, Textarea, FileInput, Select, Form, DateField, ClearableFileInput, ValidationError, CharField, CheckboxInput
from django.forms.models import inlineformset_factory, modelformset_factory, BaseModelFormSet
from .models import *
from accounting.models import *
from django.utils.timezone import now


class ChildForm(ModelForm):
    class Meta:
        model = Children
        fields = ['fullname', 'slug', 'date_of_birth', 'growth', 'image', 'weight', 'date_start', 'date_end', 'address', 'actual_group']
        widgets = {
            'date_of_birth': SelectDateWidget(years=range(2000, now().year + 1)),
            'address': Textarea(),
            'image': FileInput(),
            'actual_group': Select(),
            'date_start': DateInput(attrs={"class": "cl-date-picker"}),
            'date_end': DateInput(attrs={"class": "cl-date-picker"})}

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-wrp'
            if visible.name == 'relation':
                visible.field.widget.attrs['class'] = 'disabled-text-area'
            if visible.name == 'address':
                visible.field.widget.attrs['class'] = 'non-resize-text-area'
            if visible.name == 'date_start':
                visible.field.widget.attrs['class'] = 'input-wrp cl-date-picker'
            if visible.name == 'date_end':
                visible.field.widget.attrs['class'] = 'input-wrp cl-date-picker'

    def clean(self):
        if 'date_start' in self.fields:
            if not self.cleaned_data["date_start"]:
                raise ValidationError("Заповніть дату початку навчання у садочку", code="Field empty")
        if 'actual_group' in self.fields:
            if not self.cleaned_data["actual_group"]:
                raise ValidationError("Оберіть із списку групу", code="Field empty")
                # self.add_error('date_start', "Заповніть дату початку навчання у садочку")

        return self.cleaned_data




class BaseParentFormSet(BaseModelFormSet):
    address = CharField(max_length=250, required=False, empty_value='')

    class Meta:
        model = Parent
        fields = ['fullname', 'date_of_birth', 'phone', 'relation', 'address', 'work', 'workplace']
        # exclude = ['id']
    #
    # def __init__(self, *args, **kwargs):
    #     super(BaseParentFormSet, self).__init__(*args, **kwargs)
    #     for form in self.forms:
    #         print('ddddddd')
    #         print(form)



ParentFormSet = inlineformset_factory(
    Children,
    Parent,
    # form=ChildForm,
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


class BasePaymentChildGroupFormSet(BaseModelFormSet):
    class Meta:
        model = ChildPaymentGroup
        field = ['child', 'payment_group', 'date_start', 'date_end', 'enable']

PaymentChildGroupFormSet = inlineformset_factory(
    Children,
    ChildPaymentGroup,
    fields=['payment_group', 'date_start', 'date_end', 'enable'],
    extra=0,
    formset=BasePaymentChildGroupFormSet,
    can_delete=True,
    widgets={
        'payment_group': Select(),
        'date_start': DateInput(attrs={"class": "cl-date-picker"}),
        'date_end': DateInput(attrs={"class": "cl-date-picker"}),
        'enable': CheckboxInput(attrs={'onclick':"return false;"})
    },
    localized_fields=['date_start', 'date_end']
)