# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import ProcessFormView

app_name = 'plugin_form_handler'

urlpatterns = [
    url(r'^(?P<plugin_id>\d+)/$', ProcessFormView.as_view(), name='process_form'),
]
