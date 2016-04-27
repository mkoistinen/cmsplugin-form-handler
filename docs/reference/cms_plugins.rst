-----------------------------------------
:mod:`cmsplugin_form_handler.cms_plugins`
-----------------------------------------

.. module:: cmsplugin_form_handler.cms_plugins

This module contains an alternative super-class for CMS plugins that
encapsulates all plugin-related cmsplugin-form-handler logic.

FormPluginBase
--------------

.. class:: FormPluginBase()

This class is a sub-class of the normal ``cms.plugin_base.CMSPluginBase`` but
offers additional functionality for dealing with plugin-based forms.

Attributes
**********

.. attribute:: cache

    This base-class will automatically set the normal ``cache`` attribute to
    ``False``. This can be overridden in the project's plugin class, but it is
    not recommended because presenting a form should also include a CSRF token,
    which should never be cached.

.. attribute:: form_class

    Set this to the ``forms.Form`` or ``forms.ModelForm`` you wish this plugin
    to present. If you need to determine which form to present based on the
    specific plugin instance, see :meth:`get_form_class`.

.. attribute:: success_url

    Set this to the URL of the "success page" of the form. Using this attribute
    is simple and suitable for static success URLs. However, in most projects,
    it is likely more appropriate to use :meth:`get_success_url`.

Methods
*******

.. method:: get_form_class(request, instance)

    Returns the class of the form that this plugin presents. The default
    implementation of this method is to simply return the contents of
    :attr:`form_class`. Override this method if different plugins instances of
    the same plugin class should return different forms.

    :param HTTPRequest request:

        This is the request object for the form-submission. This may be useful
        for making a determination about which form class to return.

    :param CMSPlugin instance:

        This is the CMS plugin instance of the plugin used to produce the form.

.. method:: get_success_url(request, instance)

    Returns the desired URL that the user should be redirected to if their form
    submission validates.

    :param HTTPRequest request:

        This is the request object for the form-submission. This may be useful
        for making a determination about which success URL to return.

    :param CMSPlugin instance:

        This is the CMS plugin instance of the plugin used to produce the form.
        (Hint: you could present a list of choices in the ``CMSPlugin``model
        using a ``cms.models.fields.PageField``.)

    The default implementation of this method is to simply return the contents
    of :attr:`success_url`, but in most cases, a static URL is inappropriate.
    For example, it may be better to return the absolute URL of a specific CMS
    page (which could be moved by the content managers to different paths). In
    this case, something like this may be useful: ::

        # NOTE: only relevant code is shown here...

        from cms.models import Page
        from cms.utils import get_language_from_request
        from cms.utils.i18n import get_default_language

        from cmsplugin_form_handler.cms_plugins import FormPluginBase

        class SomePlugin(FormPluginBase):
            ...
            success_url = '/'  # a sane default
            ...

            def get_success_url(self, request, instance):
                # Be sure to set this in the Advanced Settings tab of the
                # desired CMS Page.
                reverse_id = 'success_page'

                # We'll need to know which language is relevant...
                lang = get_language_from_request(request) or get_default_language()

                try:
                    page = Page.objects.get(
                        reverse_id=reverse_id,
                        publisher_is_draft=False
                    )
                except Page.DoesNotExist:
                    # Can't find the success page, return the something sane...
                    return self.success_url
                else:
                    return page.get_absolute_url(lang)

    Or, as hinted above, you could use the CMSPlugin model to present a set of
    choices using a ``cms.models.fields.PageField`` to the Content Manager when
    creating the plugin instance, then, use the ``get_success_url`` method to
    return the absolute URL of the selected choice.

.. method:: form_valid(request, instance, form)

    This method is called if the form is valid.

    :param HTTPRequest request:

        This is the request object for the form-submission. This may be useful
        for determining what to do with the valid form.

    :param CMSPlugin instance:

        This is the CMS plugin instance of the plugin used to produce the form.

    :param Form form:

        This is the validated form.


    The default implementation simply calls the ``save`` method on the form.
