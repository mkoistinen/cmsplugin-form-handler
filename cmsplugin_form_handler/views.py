# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from urllib.parse import urlparse, urlencode  # py3
except ImportError:
    from urlparse import urlparse  # py2
    from urllib import urlencode  # py2

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic import FormView

from cms.models import CMSPlugin

from . import get_session_key


class ProcessFormView(FormView):
    """
    The goal of this view is to accept a POSTed form. From this, determine which
    CMSPlugin it belongs to, grab the form class, instantiate the form, validate
    it as normal, then, if valid, redirect to the `success_url` as defined in
    the plugin class's get_success_url(instance).

    If the form is not valid, then send it back whence it came.
    """
    http_method_names = ['post', 'put', ]

    @cached_property
    def plugin(self):
        """
        Returns (instance, plugin) for the source plugin if found, else 404.
        """
        try:
            plugin_id = int(self.kwargs.get('plugin_id'))
            cms_plugin_instance = CMSPlugin.objects.get(pk=plugin_id)
        except (KeyError, TypeError, CMSPlugin.DoesNotExist) as e:
            raise ImproperlyConfigured('Source form plugin not found.')
        return cms_plugin_instance.get_plugin_instance()

    @cached_property
    def source_url(self):
        source_url = self.request.POST.get('cmsplugin_form_source_url')
        return source_url

    def get_form_class(self):
        instance, plugin = self.plugin
        if hasattr(plugin, 'get_form_class'):
            return plugin.get_form_class(self.request, instance)
        raise ImproperlyConfigured(
            'Source form plugin does not define `get_form_class()`.')

    def get_form_kwargs(self):
        kwargs = super(ProcessFormView, self).get_form_kwargs()
        kwargs['source_url'] = self.source_url
        return kwargs

    def get_success_url(self):
        instance, plugin = self.plugin
        try:
            url = plugin.get_success_url(self.request, instance)
            return url
        except AttributeError:
            raise ImproperlyConfigured(
                'Source plugin does not define `get_success_url()`.')

    def get_form_valid(self):
        """
        Returns the `form_valid()` callback as a bound method from the
        source plugin.
        """
        instance, plugin = self.plugin
        try:
            callback = plugin.valid_form(self.request, instance)
            return callback
        except AttributeError:
            return None

    def form_valid(self, form):
        """
        Send the validated form back to the plugin for handling before
        redirecting to the `success_url`.
        """
        # Clean up our session var as it is no longer relevant.
        if hasattr(self.request, 'session'):
            session_key = get_session_key(self.plugin[0].pk)
            if session_key in self.request.session:
                del self.request.session[session_key]

        # If the source plugin has declared a `form_valid` method, call it with
        # the validated form before redirecting to the `success_url`.
        instance, plugin = self.plugin
        plugin.form_valid(self.request, instance, form)

        return super(ProcessFormView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Return to sender
        """
        plugin_id = self.plugin[0].pk
        url = self.source_url
        data = form.data.copy()
        if getattr(self.request, 'session'):
            session_key = get_session_key(plugin_id)
            self.request.session[session_key] = data
        else:
            # Fallback to GET params...
            # Don't need this on the URL
            del data['csrfmiddlewaretoken']
            # We will need this though.
            data['cmsplugin_form_plugin_id'] = plugin_id

            params = urlparse(url)
            params.update(data)
            url = '{0}?{1}'.format(self.source_url, params)
        return redirect(url)
