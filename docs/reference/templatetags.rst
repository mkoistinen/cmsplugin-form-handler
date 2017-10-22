--------------------------------------------------------------
:mod:`cmsplugin_form_handler.templatetags.cmsplugin_form_tags`
--------------------------------------------------------------

.. module:: cmsplugin_form_handler.templatetags.cmsplugin_form_tags

This module contains template tags that are provided by this package.


.. templatetag:: form_action

form_action
-----------

This template tag provides the URL for the form action. It simply returns the
correct URL to use for submitting the form. It is roughly equivalent to: ::

    {% url 'cmsplugin_form_handler:process_form' instance.pk %}

Although simple, the purpose of this tag is to encapsulate the implementation
details of cmsplugin-form-handler so that future changes can occur as necessary
without breaking existing projects.

    :param int plugin_pk:

        This can be used to specify the ID of the plugin that the view should
        use to process the form. If the developer uses CMS development
        conventions, this parameter should never be necessary. However, there
        may be some cases where the ``render()`` method uses a variable other
        than ``instance`` in its context. In these cases, it may be necessary to
        use that variable in this template tag as follows: ::

            # In this example, the context includes the variable ``plugin``
            # that contains the plugin instance to render

            {% load cmsplugin_form_tags %}
            ...
            <form action="{% form_action plugin %}" method="post">

