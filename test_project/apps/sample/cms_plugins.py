# -*- coding: utf-8 -*-

from cmsplugin_form_handler.cms_plugins import FormPluginBase
from cms.plugin_pool import plugin_pool

from .forms import SampleForm


class SamplePlugin(FormPluginBase):
    render_template = 'sample/plugins/sample_plugin.html'
    form_class = SampleForm
    success_url = '/'  # Or, see: get_success_url()
    name = 'Sample Plugin'

    def render(self, context, instance, placeholder):
        context = super(SamplePlugin, self).render(context, instance, placeholder)
        return context

    def get_form_class(self, request, instance):
        # Use this method to programmatically determine the form_class.
        # This is what this method does by default:
        return self.form_class

    def get_form_kwargs(self, request, instance):
        # Use this method to programmatically add additional parameters to
        # your form. By default, this should return an empty dict.
        return {}

    def get_success_url(self, request, instance):
        # Use this method to programmatically determine the success_url.
        # This is what this method does by default:
        return self.success_url

    def form_valid(self, request, instance, form):
        # Optionally do something with the rendered form here
        # This is what this method does by default:
        form.save()


plugin_pool.register_plugin(SamplePlugin)
