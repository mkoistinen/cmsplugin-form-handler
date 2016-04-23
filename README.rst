===================
PLUGIN_FORM_HANDLER
===================

.. important::

    This is only a Proof-of-concept, but it works!


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
    from cmsplugin_form_handler.forms import FormPluginFormBase


    class CoolForm(FormPluginFormBase):
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

    <h2>Form Plugin ({{ instance.pk }})</h2>
    <form action="{{ plugin_form_action }}" method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>

Note that the only thing special here is the extra context:
``plugin_form_action`` and ``form``.
