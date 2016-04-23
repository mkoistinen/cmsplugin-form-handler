# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from cms.plugin_base import CMSPluginBase


class FormPluginBase(CMSPluginBase):
    """
    Subclass this to prepare a plugin to be used for form handling.
    """
    cache = False

    # These should be overridden in sub-classes
    form_class = None
    success_url = None

    def get_form_class(self, instance):
        """
        Override in subclass as required
        """
        return self.form_class

    def get_success_url(self, instance):
        """
        Override in subclass as required
        """
        return self.success_url

    def render(self, context, instance, placeholder):
        context = super(FormPluginBase, self).render(context, instance, placeholder)
        request = context.get('request')
        form_class = self.get_form_class(instance)

        if form_class:
            context['cmsplugin_form_handler_action'] = reverse(
                'cmsplugin_form_handler:process_form', args=(instance.pk, ))
            instance_id = request.GET.get('instance_id')
            if instance_id and int(instance_id) == instance.pk:
                data = request.GET.copy()
                context['form'] = form_class(instance, data=data)
            else:
                context['form'] = form_class(instance)
        return context
