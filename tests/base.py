# -*- coding: utf-8 -*-

import random
import string

from test_project.apps.sample.cms_plugins import SamplePlugin

from cms.api import create_page, add_plugin, publish_page
from cms.models import Title
from cms.models.pluginmodel import CMSPlugin
from cms.test_utils.testcases import CMSTestCase


class CMSPluginFormHandlerTestCase(CMSTestCase):

    def setUp(self):
        """
        Create basic page with our plugin, if not already present.
        """
        super(CMSPluginFormHandlerTestCase, self).setUp()

        # Get user capable of creating pages and installing plugins
        superuser = self.get_superuser()

        # Create page if not present
        page = None
        self.page_title_text = 'Basic Form Page'
        if not Title.objects.filter(title=self.page_title_text).exists():
            page = create_page(
                self.page_title_text,
                'fullwidth.html',
                'en',
                published=True,
            )
        assert page

        # Get placeholder from the page
        placeholder = page.placeholders.filter(slot='content').first()
        assert placeholder

        # Ensure our plugin is installed
        if not CMSPlugin.objects.filter(placeholder=placeholder):
            plugin = add_plugin(placeholder, SamplePlugin, 'en')
            assert plugin

        # Ensure page is published
        publish_page(page, superuser, 'en')

    def get_random_string(self, length=10):
        """
        Quick-n-dirty random string generation.
        """
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for _ in range(length)])
