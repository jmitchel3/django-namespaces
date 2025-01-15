from __future__ import annotations

from django.test import override_settings
from django.test import TestCase

from django_namespaces.conf import get_settings
from django_namespaces.conf import Settings
from django_namespaces.conf import settings


class SettingsTests(TestCase):
    def test_singleton_settings(self):
        """Test that get_settings returns the same instance"""
        settings1 = get_settings()
        settings2 = get_settings()
        self.assertIs(settings1, settings2)
        self.assertIs(settings, settings1)

    def test_default_settings(self):
        """Test default values for all settings"""
        s = Settings()

        self.assertEqual(
            s.DJANGO_NAMESPACES_NAMESPACE_MODEL,
            "django_namespaces.Namespace",
        )
        self.assertEqual(
            s.DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION,
            "django_namespaces.blocked.blocked_namespaces",
        )
        self.assertEqual(
            s.DJANGO_NAMESPACES_NEEDS_ACTIVATION_TEMPLATE,
            "django_namespaces/namespace_needs_activation.html",
        )
        self.assertEqual(s.DJANGO_NAMESPACES_MAX_HANDLE_LENGTH, 50)
        self.assertEqual(
            s.DJANGO_NAMESPACES_CREATE_FORM,
            "django_namespaces.forms.NamespaceCreateForm",
        )
        self.assertEqual(
            s.DJANGO_NAMESPACES_UPDATE_FORM,
            "django_namespaces.forms.NamespaceUpdateForm",
        )
        self.assertEqual(
            s.DJANGO_NAMESPACES_URL_REVERSE_FUNCTION, "django.urls.reverse"
        )
        self.assertEqual(s.DJANGO_NAMESPACES_ACTIVATION_REDIRECT_URL, "/")
        self.assertEqual(s.DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS, 3600)
        self.assertEqual(
            s.DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX, "dj:namespace:qs:"
        )

    @override_settings(
        DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION="custom.blocked",
        DJANGO_NAMESPACES_NEEDS_ACTIVATION_TEMPLATE="custom/template.html",
        DJANGO_NAMESPACES_MAX_HANDLE_LENGTH=100,
        DJANGO_NAMESPACES_CREATE_FORM="custom.CreateForm",
        DJANGO_NAMESPACES_UPDATE_FORM="custom.UpdateForm",
        DJANGO_NAMESPACES_URL_REVERSE_FUNCTION="custom.reverse",
        DJANGO_NAMESPACES_ACTIVATION_REDIRECT_URL="/custom/",
        DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS=7200,
        DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX="custom_prefix_",
    )
    def test_custom_settings(self):
        """Test that custom settings override defaults"""
        s = Settings()

        self.assertEqual(s.DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION, "custom.blocked")
        self.assertEqual(
            s.DJANGO_NAMESPACES_NEEDS_ACTIVATION_TEMPLATE, "custom/template.html"
        )
        self.assertEqual(s.DJANGO_NAMESPACES_MAX_HANDLE_LENGTH, 100)
        self.assertEqual(s.DJANGO_NAMESPACES_CREATE_FORM, "custom.CreateForm")
        self.assertEqual(s.DJANGO_NAMESPACES_UPDATE_FORM, "custom.UpdateForm")
        self.assertEqual(s.DJANGO_NAMESPACES_URL_REVERSE_FUNCTION, "custom.reverse")
        self.assertEqual(s.DJANGO_NAMESPACES_ACTIVATION_REDIRECT_URL, "/custom/")
        self.assertEqual(s.DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS, 7200)
        self.assertEqual(
            s.DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX, "custom_prefix_"
        )
