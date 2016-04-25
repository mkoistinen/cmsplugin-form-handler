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

        def get_form_class(self, instance):
            # Use this method to programmatically determine the form_class.
            # This is what this method does by default:
            return self.form_class

        def get_success_url(self, instance):
            # Use this method to programmatically determine the success_url.
            # This is what this method does by default:
            return self.success_url

        def form_valid(self, instance, form):
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



