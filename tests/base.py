# -*- coding: utf-8 -*-

import random
import string

from cms.api import create_page, add_plugin, publish_page
from cms.models import Title
from cms.models.pluginmodel import CMSPlugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_text_ckeditor.cms_plugins import TextPlugin

from test_project.apps.sample.cms_plugins import (
    SampleFormPlugin, SampleModelFormPlugin, SampleCrispyModelFormPlugin)


class CMSPluginFormHandlerTestCase(CMSTestCase):

    def setUp(self):
        """
        Create basic page with our plugin, if not already present.

        Also, adds these instance properties:

            self.page: Published page instance
            self.form_plugin : Public version of a SamplePlugin instance
            self.model_form_plugin: Public SampleModelForm instance.
            self.crispy_model_form_plugin: Public SampleCrispyModelForm inst.
        """
        super(CMSPluginFormHandlerTestCase, self).setUp()

        # Get user capable of creating pages and installing plugins
        superuser = self.get_superuser()

        # Create page if not present
        page = None
        page_title_text = 'Basic Form Page'
        if not Title.objects.filter(title=page_title_text).exists():
            page = create_page(
                page_title_text,
                'fullwidth.html',
                'en',
                published=False,
            )

        # Get placeholder from the page
        placeholder = page.placeholders.filter(slot='content').first()
        assert placeholder

        # Ensure our plugin is installed
        if not CMSPlugin.objects.filter(placeholder=placeholder):
            add_plugin(placeholder, SampleFormPlugin, 'en')
            add_plugin(placeholder, SampleModelFormPlugin, 'en')
            add_plugin(placeholder, SampleCrispyModelFormPlugin, 'en')
            add_plugin(placeholder, TextPlugin, 'en')

        # Ensure we have the public version of the page
        page = publish_page(page, superuser, 'en')
        self.page = page.publisher_public
        assert not self.page.publisher_is_draft

        # Get published versions of the plugins
        self.plugin = self.crispy_plugin = None
        for ph in self.page.placeholders.filter(slot='content'):
            for plugin in ph.get_plugins_list():
                klass = plugin.get_plugin_class()
                if klass == SampleFormPlugin:
                    self.form_plugin = plugin
                elif klass == SampleModelFormPlugin:
                    self.model_form_plugin = plugin
                elif klass == SampleCrispyModelFormPlugin:
                    self.crispy_model_form_plugin = plugin
                elif klass == TextPlugin:
                    self.text_plugin = plugin

        assert self.form_plugin
        assert self.model_form_plugin
        assert self.crispy_model_form_plugin
        assert self.text_plugin

    @staticmethod
    def get_random_string(length=10):
        """
        Quick-n-dirty random string generation.
        """
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for _ in range(length)])
