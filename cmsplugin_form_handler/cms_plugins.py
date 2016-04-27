# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase

from . import get_session_key


class FormPluginBase(CMSPluginBase):
    """
    Subclass this to prepare a plugin to be used for form handling.
    """
    cache = False

    # These should be overridden in sub-classes
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
        context = super(FormPluginBase, self).render(context, instance, placeholder)  # noqa
        request = context.get('request')

        form_class = self.get_form_class(request, instance)
        if form_class:
            source_url = request.get_full_path()
            data = None

            if hasattr(request, 'session'):
                data = request.session.get(get_session_key(instance.pk))
            elif request.GET.get('cmsplugin_form_plugin_id'):
                # Sessions aren't available, see if we fell-back to GET params
                plugin_id = request.GET.get('cmsplugin_form_plugin_id')
                if plugin_id and int(plugin_id) == instance.pk:
                    data = request.GET.copy()

            if data:
                context['cmsplugin_form'] = form_class(source_url, data=data)
            else:
                context['cmsplugin_form'] = form_class(source_url)
        return context
