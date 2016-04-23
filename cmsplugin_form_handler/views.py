# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import urllib.parse

from django.shortcuts import Http404, redirect
from django.views.generic import FormView

from cms.models import CMSPlugin


class ProcessFormView(FormView):
    """
    The goal of this view is to accept a POSTed form. From this, determine which
    CMSPlugin it belongs to, grab the form class, instantiate the form, validate
    it as normal, then, if valid, redirect to the `success_url` as defined in
    the plugin class's get_success_url(instance).

    If the form is not valid, then send it back whence it came.
    """
    http_method_names = ['post', ]

    def get_plugin(self):
        """
        Returns (instance, plugin) for the source plugin if found, else 404.
        """
        if self.kwargs['instance_id']:
            cms_plugin_instance = CMSPlugin.objects.get(pk=self.kwargs['instance_id'])
            return cms_plugin_instance.get_plugin_instance()
        raise Http404('Source plugin not found.')

    def get_form_class(self):
        instance, plugin = self.get_plugin()
        if hasattr(plugin, 'get_form_class'):
            return plugin.get_form_class(instance)
        else:
            raise Http404('Source plugin does not define `get_form_class()`.')

    def get_form_kwargs(self):
        kwargs = super(ProcessFormView, self).get_form_kwargs()
        kwargs['instance_id'] = self.kwargs['instance_id']
        return kwargs

    def get_source_url(self):
        url_obj = urllib.parse.urlparse(self.request.META.get('HTTP_REFERER'))
        return url_obj.path

    def get_success_url(self):
        instance, plugin = self.get_plugin()
        if hasattr(plugin, 'get_success_url'):
            url = plugin.get_success_url(instance)
            return url
        raise Http404('Source plugin does not define `get_success_url()`.')

    def form_invalid(self, form):
        """
        Return to sender
        """
        # Probably don't need this on the URL
        data = form.data.copy()
        del(data['csrfmiddlewaretoken'])

        url = '{0}?{1}'.format(
            self.get_source_url(),
            urllib.parse.urlencode(data),
        )
        return redirect(url)
