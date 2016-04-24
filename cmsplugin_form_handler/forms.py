# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms


class FormPluginFormMixin(object):
    def __init__(self, source_url, *args, **kwargs):
        super(FormPluginFormMixin, self).__init__(*args, **kwargs)
        self.fields['cmsplugin_form_source_url'] = forms.CharField(widget=forms.HiddenInput, initial=source_url)
