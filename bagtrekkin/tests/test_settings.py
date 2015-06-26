from django.apps import apps
from django.test import TestCase
from django.test.utils import override_settings


class SettingsResourceTestCase(TestCase):

    @override_settings(DEBUG=True)
    def test_debug_true(self):
        self.assertTrue(apps.is_installed('debug_toolbar'))
