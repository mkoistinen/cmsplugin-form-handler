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

A templatetag (``cmsplugin_form_action``) is provided to include the special
URL as the ``action`` of the form making the encapsulation complete.


Use with other packages
-----------------------

Use with third-party packages such as Crispy Forms is possible, please see
:ref:`crispy-forms`.
