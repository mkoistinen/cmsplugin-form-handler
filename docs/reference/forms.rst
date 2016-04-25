-----------------------------------
:mod:`cmsplugin_form_handler.forms`
-----------------------------------

.. module:: cmsplugin_form_handler.forms

FormPluginFormMixin
-------------------

This module contains code that encapsulates the cmsplugin-forms-handler
functionality relating to forms.

.. class:: FormPluginFormMixin(source_url, *args, **kwargs)

This class is a form "mixin" that may be applied to ``forms.Form`` or
``forms.ModelForm`` classes. The mixin embeds a hidden field for passing the
source URL which is required for the correct operation of this package.

It also modifies the constructor signature of the form by adding a new, required
arg: source_url, but in most cases, this is transparently dealt with by the
package.
