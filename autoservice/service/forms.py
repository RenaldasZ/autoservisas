from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('content', 'order', 'reviewer')
        widgets = {
            'order': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }


class OrderCreateForm(forms.ModelForm):
    # service = forms.ModelChoiceField(queryset=models.Service.objects.all(), empty_label=None)
    class Meta:
        model = models.Order
        fields = ('car', 'due_back', 'price')
        widgets = {
            'due_back': DateInput(),
            'price': forms.HiddenInput(),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ('model', 'vin_code', 'licence_plate', 'note')
        widgets = {
            'due_back': DateInput(),
        }


class OrderEntryCreateForm(forms.ModelForm):
    class Meta:
        model = models.OrderEntry
        fields = ("service", "order")
        widgets = {
        'order': forms.HiddenInput(),
        }
