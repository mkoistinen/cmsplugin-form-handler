---------------------------------
Third Party Package Compatibility
---------------------------------

.. _crispy-forms:

Crispy Forms
------------

`django-crispy-forms <http://django-crispy-forms.readthedocs.io/en/latest/index.html>`_
(`repo <https://github.com/django-crispy-forms/django-crispy-forms>`_) is a
full-featured and rather popular form rendering package. Since Crispy Forms
renders the entire form including the form-tags, use of the
``cmsplugin_form_action`` templatetag isn't really an option.

The ``cmsplugin_form_action`` templatetag is provided as a convenience, but it
is possible to determine the correct action URL without it. The following is an
example Crispy Form and FormPluginFormMixin enabled ModelForm for a
CMS plugin: ::

    from django import forms
    from django.core.urlresolvers import reverse

    from cmsplugin_form_handler.forms import FormPluginFormMixin
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    from .models import Sample

    class SampleForm(FormPluginFormMixin, forms.ModelForm):
       class Meta:
           model = Sample
           fields = '__all__'  # for brevity

       # NOTE: Notice that the signature of `__init__()` must match the one in
       # the FormPluginFormMixin and include: `source_url` and `instance`
       def __init__(self, source_url, instance, **kwargs):
           super(SampleForm, self).__init__(source_url, instance, **kwargs)
           self.helper = FormHelper()

           # NOTE: The url pattern is provide by cmsplugin-form-handler and
           # `self.plugin_id` is an attribute provided by
           # the FormPluginFormMixin:
           self.helper.form_action = reverse(
              'cmsplugin_form_handler:process_form',
               args=(self.plugin_id, )
           )

           self.helper.attrs = {'novalidate': 'novalidate'}
           self.helper.add_input(Submit('submit', 'Submit'))
