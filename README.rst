======================
CMSPlugin Form Handler
======================

|PyPI Version| |Build Status| |Coverage Status|

.. |PyPI Version| image:: http://img.shields.io/pypi/v/cmsplugin-form-handler.svg
   :target: https://pypi.python.org/pypi/cmsplugin-form-handler
.. |Build Status| image:: http://img.shields.io/travis/mkoistinen/cmsplugin-form-handler/master.svg
   :target: https://travis-ci.org/mkoistinen/cmsplugin-form-handler
.. |Coverage Status| image:: http://img.shields.io/coveralls/mkoistinen/cmsplugin-form-handler/master.svg
   :target: https://coveralls.io/r/mkoistinen/cmsplugin-form-handler?branch=master


This package provides a mechanism for handling form-submissions in
django-CMS plugins.

Jump to `Quickstart`_ below to get started, or see the proper
`documentation <http://cmsplugin-form-handler.readthedocs.org/en/latest/>`_.

---------------------
Background & Approach
---------------------

.. Avoid non-standard directives (like those from Sphinx) here, as this file is
   also `include`d in the project's README.txt file.

Background
----------

Plugins are a key component of `django CMS <https://django-cms.org>`_ for
creating reusable, configurable content fragments in django CMS projects. Due to
their flexibility and utility, project developers would benefit from emitting
forms and handling form submissions using plugins.

Since CMS plugins are fragments of a page, they do not provide a unique, URL for
receiving and handling form submissions. This presents numerous challenges when
attempting to process form submissions.


Approach
--------

To get around these limitations, the approach taken in this package is to direct
form submissions from plugins which sub-class ``FormPluginBase`` to a URL that
is outside of the django CMS URL-space and handled by a ``ProcessFormView``
provided by this package.

The ``ProcessFormView`` accepts form-submissions, processes them, and if valid,
sends the resulting form back to the plugin class for handling and then responds
to the request with a redirect to a ``success_url`` provided by the plugin.

On validation errors, the view will redirect the request back to the originating
page and provide the form data via a session variable back to the plugin's form.

The user experience is precisely as expected and the handling of the form is
performed without "thrown HTTPRedirectResponses" or any special middleware.

This package encapsulates all extra logic so that the plugin developer need
only to subclass ``FormPluginBase`` rather than the usual
``cms.plugin_base.CMSPluginBase``.

The ``Form`` or ``ModelForm`` presented in the CMS plugin should also include
the "mixin" ``FormPluginFormMixin``.


----------
Quickstart
----------

.. Avoid non-standard directives (like those from Sphinx) here, as this file is
   also `include`d in the project's README.txt file.

To get started quickly, first install the package: ::

    pip install cmsplugin-form-handler

Add the package to ``settings.INSTALLED_APPS``: ::

    # my_cool_project/settings.py

    INSTALLED_APPS = (
        ...
        'cmsplugin_form_handler',
    )

Add an extra line in your url configuration: ::

    urlpatterns = i18n_patterns('',
        url(r'^admin/', include(admin.site.urls)),
        ...
        url(r'^plugin_forms/', include('cmsplugin_form_handler.urls',
                                       namespace='cmsplugin_form_handler')),
        url(r'^', include('cms.urls')),
    )


Add the ``FormPluginFormMixin`` mixin to your ``Form``: ::

    # my_cool_project/forms.py

    from django import forms
    from cmsplugin_form_handler.forms import FormPluginFormMixin

    class MyCoolForm(FormPluginFormMixin, forms.Form):
        # everything else is your normal form.
        my_cool_field = forms.CharField(...)
        ...

Or, if you're using a ``ModelForm``: ::

    # my_cool_project/forms.py

    from django import forms
    from cmsplugin_form_handler.forms import FormPluginFormMixin

    class MyCoolModelForm(FormPluginFormMixin, forms.ModelForm):
        # everything else is your normal form.
        class Meta:
            model = MyCoolModel
        ...

Subclass your cms plugin from ``FormPluginBase``: ::

    # my_cool_project/cms_plugins.py

    from cmsplugin_form_handler.cms_plugins import FormPluginBase

    class MyCoolPlugin(FormPluginBase):
        # Use your normal CMSPlugin attributes...
        render_template = 'plugins/my_cool_plugin.html'
        # Note that ``cache = False`` will automatically be set

        # These should be overridden in sub-classes
        form_class = MyCoolForm  # Or, see: get_form_class()
        success_url = '/static/success/url/here'  # Or, see: get_success_url()

        def render(self, context, instance, placeholder):
            context = super(MyCoolPlugin, self).render(context, instance, placeholder)

            # Do your normal thing here
            ...

            return context

        def get_form_class(self, request, instance):
            # Use this method to programmatically determine the form_class.
            # This is what this method does by default:
            return self.form_class

        def get_success_url(self, request, instance):
            # Use this method to programmatically determine the success_url.
            # This is what this method does by default:
            return self.success_url

        def form_valid(self, request, instance, form):
            # Optionally do something with the rendered form here
            # This is what this method does by default:
            form.save()


Finally, update your plugin's template: ::

    # my_cool_project/templates/plugins/my_cool_plugin.html

    {% load cmsplugin_form_tags %}

    <h2>Form Plugin</h2>
    <form action="{% cmsplugin_form_action %}" method="post">
        {% csrf_token %}
        {{ cmsplugin_form }}
        <input type="submit">
    </form>
