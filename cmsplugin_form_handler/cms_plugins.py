# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import QueryDict

from cms.plugin_base import CMSPluginBase

from . import get_session_key


class FormPluginBase(CMSPluginBase):
    """
    Subclass this to prepare a plugin to be used for form handling.
    """
    # Caching a plugin that has a form doesn't make sense, so, it is disabled
    # here. It can, however, be overridden in the sub-class if necessary.
    cache = False

    # These should be overridden in sub-classes unless the getter-equivalent
    # is defined instead
    form_class = None
    success_url = None

    def get_form_class(self, request, instance):
        """
        Returns the form class to be used by this plugin.

        Default implementation is to return the contents of
        FormPluginBase.form_class, but this method can be overridden as
        required for more elaborate circumstances.
        """
        return self.form_class

    def get_form_kwargs(self, request, instance):
        """
        Returns any additional kwargs to add to the form.

        Default implementation is to return an empty dict.
        """
        return {}

    def get_success_url(self, request, instance):
        """
        Returns the redirect URL for successful form submissions.

        Default implementation is to return the contents of
        FormPluginBase.success_url, but this method can be overridden as
        required for more elaborate circumstances.
        """
        return self.success_url

    def form_valid(self, request, instance, form):
        """
        If the form validates, this method will be called before the user is
        redirected to the success_url. The default implementation is to just
        save the form.
        """
        form.save()

    def render(self, context, instance, placeholder):
        context = super(FormPluginBase, self).render(
            context, instance, placeholder)
        request = context.get('request')

        form_class = self.get_form_class(request, instance)
        if form_class:
            source_url = request.get_full_path()
            data = None

            if hasattr(request, 'session'):
                data = request.session.get(get_session_key(instance.pk))
                try:
                    data = QueryDict(data)
                except TypeError:
                    # the data must have already been saved as a dict. Just
                    # use the dict until a string is saved
                    pass
            elif request.GET.get('cmsplugin_form_plugin_id'):
                # Sessions aren't available, see if we fell-back to GET params
                plugin_id = request.GET.get('cmsplugin_form_plugin_id')
                if plugin_id and int(plugin_id) == instance.pk:
                    data = request.GET.copy()

            kwargs = self.get_form_kwargs(request, instance)
            kwargs.update({
                'source_url': source_url,
                'instance': instance,
            })
            if data:
                kwargs.update({'data': data})
            context['cmsplugin_form'] = form_class(**kwargs)
        return context
