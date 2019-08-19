# -*- coding: utf-8 -*-

from django import forms
from django.urls import reverse

from cmsplugin_form_handler.forms import FormPluginFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Sample


class SampleForm(FormPluginFormMixin, forms.Form):
    """
    Simple Non-ModelForm.
    """
    name = forms.CharField(max_length=20, required=True)
    message = forms.CharField(max_length=1000, widget=forms.Textarea())


class SampleModelForm(FormPluginFormMixin, forms.ModelForm):
    """
    Simple ModelForm.
    """
    class Meta:
        model = Sample
        fields = '__all__'


class SampleCrispyModelForm(SampleModelForm):
    """
    Same Simple ModelForm, but uses Django Crispy Forms.
    """
    def __init__(self, source_url, instance, **kwargs):
        super(SampleCrispyModelForm, self).__init__(
            source_url, instance, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': 'novalidate'}
        self.helper.form_action = reverse(
            'cmsplugin_form_handler:process_form', args=(self.plugin_id, ))
        self.helper.add_input(Submit('submit', 'Submit'))
