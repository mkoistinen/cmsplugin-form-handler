# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms


class FormPluginFormBase(forms.Form):
    instance_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, instance_id, *args, **kwargs):
        super(FormPluginFormBase, self).__init__(*args, **kwargs)
        self.fields['instance_id'].initial = instance_id
