# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.urls import reverse

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

register = template.Library()


class FormAction(AsTag):
    name = 'cmsplugin_form_action'
    options = Options(
        Argument('plugin_id', required=False, resolve=False),
        'as',
        Argument('varname', required=False, resolve=False),
    )

    def get_value(self, context, **kwargs):
        """
        If no «plugin_id» is provided, then set plugin_id to `instance.pk`
        where `instance` comes from the context and is the plugin instance
        which is conventionally added to the context in CMSPluginBase.render().
        """
        plugin_id = kwargs.get('plugin_id')
        if not plugin_id and 'instance' in context:
            plugin_id = context.get('instance').pk
        return reverse(
            'cmsplugin_form_handler:process_form',
            args=(plugin_id, )
        )


register.tag(FormAction)
