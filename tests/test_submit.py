# -*- coding: utf-8 -*-

from test_project.apps.sample.models import Sample

from .base import CMSPluginFormHandlerTestCase


class TestSubmit(CMSPluginFormHandlerTestCase):

    def test_form_renders(self):
        """
        Test that the form renders.
        """
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/plugin_forms/')

    def test_form_submit(self):
        """
        Test that a form submission results in an additional Sample-instance.
        """
        # First get the number Sample-instances
        current_samples = Sample.objects.count()

        sample_name = self.get_random_string(10)
        sample_msg = self.get_random_string(100)

        response = self.client.post('/plugin_forms/2/', {
            'name': sample_name,
            'message': sample_msg,
            'cmsplugin_form_source_url': '/en/',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        assert Sample.objects.count() > current_samples
