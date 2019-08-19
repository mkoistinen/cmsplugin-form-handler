# -*- coding: utf-8 -*-

from unittest import skip
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.db.models import Max
from django.test.utils import modify_settings

from cms.models import CMSPlugin

from test_project.apps.sample.models import Sample

from .base import CMSPluginFormHandlerTestCase


class TestFormPlugin(CMSPluginFormHandlerTestCase):

    def test_form_renders(self):
        """
        Test that the normal (non-Crispy) form renders.
        """
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        process_form_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.form_plugin.pk, )
        )
        self.assertContains(response, 'action="{0}"'.format(process_form_url))

    def test_form_submission(self):
        """
        Test that a (normal, non-Crispy) form submission results in an
        additional Sample instance.
        """
        # First get the number Sample-instances
        current_samples = Sample.objects.count()

        sample_name = self.get_random_string(10)
        sample_msg = self.get_random_string(100)

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.form_plugin.pk, )
        )

        response = self.client.post(action_url, {
            'name': sample_name,
            'message': sample_msg,
            'cmsplugin_form_source_url': '/en/',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        assert Sample.objects.count() > current_samples

    @skip('django-cms requires Authentication MW, which requires Session MW')
    def test_form_submission_without_sessions(self):
        """
        Test that a (normal, non-Crispy) form submission results in an
        additional Sample instance.
        """
        # Disable session MW
        # Note: This test origianlly used the override_settings context handler
        # to attempt to update the setting.  That context hanlder was used like
        # this:
        #     with override_settings(MiddleWare=MW):
        # To actually update the settings, it should have been called like this:
        #     with override_settings(MIDDLEWARE_CLASSES=MW):
        # So, as it was originally written, the test did not remove the
        # session MW

        # This modifiy_settings call does remove the session MW.  It also
        # removes Authentication MW and Message MW because they both depend
        # on Session MW.  The Toolbar MW also depends on session MW, to it had
        # to be dropped as well.

        # Running the test with this middleware configuration, an exception is
        # raised in cms/utils/moderator.py because the WSGI request object does
        # not have a user attribute (because Authentication MW is missing)

        # It appears clear that the CMS requires both Session and Auth MW,
        # so this test is marked with skip for now.
        with modify_settings(MIDDLEWARE={
            'remove': [
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'cms.middleware.toolbar.ToolbarMiddleware',
            ],
        }):
            # First get the number Sample-instances
            current_samples = Sample.objects.count()

            sample_name = self.get_random_string(10)
            sample_msg = self.get_random_string(100)

            action_url = reverse(
                'cmsplugin_form_handler:process_form',
                args=(self.model_form_plugin.pk, )
            )

            response = self.client.post(action_url, {
                'name': sample_name,
                'message': sample_msg,
                'cmsplugin_form_source_url': '/en/',
            }, follow=True)
            self.assertEqual(response.status_code, 200)
            assert Sample.objects.count() > current_samples


class TestModelFormPlugin(CMSPluginFormHandlerTestCase):

    def test_form_renders(self):
        """
        Test that the normal (non-Crispy) form renders.
        """
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        process_form_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.model_form_plugin.pk, )
        )
        self.assertContains(response, 'action="{0}"'.format(process_form_url))

    def test_form_submission(self):
        """
        Test that a (normal, non-Crispy) form submission results in an
        additional Sample instance.
        """
        # First get the number Sample-instances
        current_samples = Sample.objects.count()

        sample_name = self.get_random_string(10)
        sample_msg = self.get_random_string(100)

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.model_form_plugin.pk, )
        )

        response = self.client.post(action_url, {
            'name': sample_name,
            'message': sample_msg,
            'cmsplugin_form_source_url': '/en/',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        assert Sample.objects.count() > current_samples


class TestCrispyModelFormPlugin(CMSPluginFormHandlerTestCase):

    def test_form_renders(self):
        """
        Test that the Crispy form renders.
        """
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        process_form_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.crispy_model_form_plugin.pk, )
        )
        self.assertContains(response, 'action="{0}"'.format(process_form_url))

    def test_form_submission(self):
        """
        Test that a Crispy form submission results in an additional
        Sample instance.
        """
        # First get the number Sample-instances
        current_samples = Sample.objects.count()

        sample_name = self.get_random_string(10)
        sample_msg = self.get_random_string(100)

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.crispy_model_form_plugin.pk, )
        )

        response = self.client.post(action_url, {
            'name': sample_name,
            'message': sample_msg,
            'cmsplugin_form_source_url': '/en/',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        assert Sample.objects.count() > current_samples


class TestErrors(CMSPluginFormHandlerTestCase):

    def test_invalid_form_submission(self):
        """
        Test that the desired response occurs when the form is not valid.
        """
        # First get the number Sample-instances
        current_samples = Sample.objects.count()

        sample_name = ''
        sample_msg = self.get_random_string(100)

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.model_form_plugin.pk, )
        )

        response = self.client.post(action_url, {
            'name': sample_name,
            'message': sample_msg,
            'cmsplugin_form_source_url': '/en/',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        assert Sample.objects.count() == current_samples

    def test_invalid_form_submission_no_session(self):
        """
        Test that the desired response occurs when the form is not valid, when
        there is no session.
        """
        # First get the number Sample-instances
        current_samples = Sample.objects.count()

        sample_name = ''
        sample_msg = self.get_random_string(100)

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.model_form_plugin.pk, )
        )

        response = self.client.post(action_url, {
            'name': sample_name,
            'message': sample_msg,
            'cmsplugin_form_source_url': '/en/',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        # Ensure we didn't add any new samples
        assert Sample.objects.count() == current_samples

    def test_non_existent_plugin_submission(self):
        """
        Test that a submitting a form for a non-existent plugin meets
        defined behavior.
        """
        sample_name = self.get_random_string(10)
        sample_msg = self.get_random_string(100)

        # Get non-existent plugin ID:
        bad_id = CMSPlugin.objects.aggregate(max=Max('id'))['max'] + 1
        assert bad_id

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(bad_id + 1, )
        )

        with self.assertRaises(ImproperlyConfigured):
            self.client.post(action_url, {
                'name': sample_name,
                'message': sample_msg,
                'cmsplugin_form_source_url': '/en/',
            }, follow=True)

    def test_non_form_handler_plugin(self):
        """
        Test that attempting to submit a non-cmsplugin-form-handler plugin
        fails as expected
        """
        sample_name = self.get_random_string(10)
        sample_msg = self.get_random_string(100)

        action_url = reverse(
            'cmsplugin_form_handler:process_form',
            args=(self.text_plugin, )
        )

        with self.assertRaises(ImproperlyConfigured):
            self.client.post(action_url, {
                'name': sample_name,
                'message': sample_msg,
                'cmsplugin_form_source_url': '/en/',
            }, follow=True)
