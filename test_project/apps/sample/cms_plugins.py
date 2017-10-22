# -*- coding: utf-8 -*-

from cmsplugin_form_handler.cms_plugins import FormPluginBase
from cms.plugin_pool import plugin_pool

from .forms import SampleForm, SampleModelForm, SampleCrispyModelForm
from .models import Sample, SamplePluginModel


class SampleFormPlugin(FormPluginBase):
    """
    This is a normal (non-Crispy) non-model form plugin..
    """
    form_class = SampleForm
    model = SamplePluginModel
    name = 'Sample Form Plugin'
    render_template = 'sample/plugins/sample_plugin.html'
    success_url = '/'

    def render(self, context, instance, placeholder):
        context = super(SampleFormPlugin, self).render(
            context, instance, placeholder)
        context['plugin_name'] = self.name
        return context

    def form_valid(self, request, instance, form):
        """'Manually' create a sample object from the form data."""
        cleaned_data = form.cleaned_data
        return Sample.objects.create(
            name=cleaned_data['name'],
            message=cleaned_data['message'],
        )


plugin_pool.register_plugin(SampleFormPlugin)


class SampleModelFormPlugin(FormPluginBase):
    """
    This is a normal (non-Crispy) model form plugin.
    """
    form_class = SampleModelForm
    model = SamplePluginModel
    name = 'Sample Model Form Plugin'
    render_template = 'sample/plugins/sample_plugin.html'
    success_url = '/'

    def render(self, context, instance, placeholder):
        context = super(SampleModelFormPlugin, self).render(
            context, instance, placeholder)
        context['plugin_name'] = self.name
        return context

    # So we can ensure that the defaults work, we're intentionally not
    # overriding the following for the tests here:
    #   get_form_class()
    #   get_form_kwargs()
    #   get_success_url()
    #   form_valid()
    #
    # This is actually the typical usage pattern anyway.


plugin_pool.register_plugin(SampleModelFormPlugin)


class SampleCrispyModelFormPlugin(FormPluginBase):
    """
    This is the same form plugin as above, but uses Django Crispy Forms.
    """
    form_class = SampleCrispyModelForm
    model = SamplePluginModel
    name = 'Sample Crispy Model Form Plugin'
    render_template = 'sample/plugins/sample_crispy_plugin.html'
    success_url = '/'  # Or, see: get_success_url()

    def render(self, context, instance, placeholder):
        context = super(SampleCrispyModelFormPlugin, self).render(
            context, instance, placeholder)
        context['plugin_name'] = self.name
        return context

    # We're 'overriding' the default implementations for the these methods.

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


plugin_pool.register_plugin(SampleCrispyModelFormPlugin)
