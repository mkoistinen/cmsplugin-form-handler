======================
CMSPlugin Form Handler
======================

This package aims to provide a mechanism for handling form-submissions in
django-CMS plugins.


Background
----------

Plugins are a key component of `django CMS <https://django-cms.org>`_ for
creating reusable, configurable content fragments in django CMS projects. Due to
their flexibility and utility, project developers would benefit from emitting
forms and handling form submissions using plugins.

Since CMS plugins are fragments of a page, they do not provide a unique, RESTful
URL for receiving and handling form submissions. This presents numerous
challenges when attempting to process form submissions.


Approach
--------

To get around these limitations, the approach taken in this package is to direct
form submissions from plugins which sub-class ``FormPluginBase`` to a URL that
is outside of the django CMS URL-space and handled by a ``ProcessFormView``
provided by this package.

The ``ProcessFormView`` accepts form-submissions, processes them, and if valid,
the request is redirected to a ``success_url`` provided by the plugin. On
validation errors, the view will redirect the request back to the originating
page and provide the form data via a session variable back to the plugin's form.

The user experience is precisely as expected and the handling of the form is
performed without "thrown HTTPRedirectResponses" or special middleware.

This package encapsulates all extra logic so that the plugin developer need
only to subclass ``cmsplugin_form_handler.cms_plugins.FormPluginBase`` rather
than the usual ``cms.plugin_base.CMSPluginBase``.

The ``Form`` or ``ModelForm`` presented in the CMS plugin should also include
the "mixin" ``cmsplugin_form_handler.forms.FormPluginFormMixin``.


------------
Installation
------------

Install package into your project's path::

    pip install [TODO]

Add to your project's settings.INSTALLED_APPS::

    INSTALLED_APPS = (
        ...,
        'cmsplugin_form_handler',
    )

Also, add a line to your project's urls.py file::

    urlpatterns = i18n_patterns('',
        url(r'^admin/', include(admin.site.urls)),  # NOQA
        url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
            {'sitemaps': {'cmspages': CMSSitemap}}),
        url(r'^select2/', include('django_select2.urls')),

        # vvvvv
        url(r'^plugin_forms/', include('cmsplugin_form_handler.urls',
                                       namespace='cmsplugin_form_handler')),
        # ^^^^^
        url(r'^', include('cms.urls')),
    )

.. note::

    The URL segment ``plugin_forms`` can be anything you like but pick something
    that is unlikely to collide with a desired page slug. It should be inserted
    before the CMS urls, but after the Admin urls.

-----
Usage
-----

When you create your plugin class, instead of inheriting from CMSPluginBase,
inherit from PluginFormBase as follows::

    from django import forms

    from cms.models import CMSPlugin

    from cmsplugin_form_handler.cms_plugins import PluginFormBase
    from cmsplugin_form_handler.forms import FormPluginFormMixin


    class CoolForm(FormPluginFormMixin, forms.Form):
        # Define your form as per usual...
        cool_field = forms.CharField(...)


    class CoolFormPlugin(PluginFormBase):
        name = 'Cool Form'
        model = CMSPlugin
        render_template = 'form_plugin.html'
        form_class = CoolForm
        success_url = 'http://www.google.com/'

    plugin_pool.register_plugin(FormPlugin)

As usual, you must define a ``render_template`` for your plugin. Here's one::

    {% load cmsplugin_form_tags %}
    <h2>Form Plugin ({{ instance.pk }})</h2>
    <form action="{% cmsplugin_form_action %}" method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>

Note that the only thing special here is the extra context:
``plugin_form_action`` and ``form``.
