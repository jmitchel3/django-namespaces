from __future__ import annotations

from django.test import TestCase

from django_namespaces.import_utils import import_module_from_str


class ImportUtilsTest(TestCase):
    def test_import_three_part_path(self):
        # Test importing something like "django.contrib.auth"
        result = import_module_from_str("django.contrib.auth")
        self.assertTrue(hasattr(result, "get_user"))
        self.assertTrue(callable(result.get_user))

    def test_import_two_part_path(self):
        # Test importing something like "django.contrib"
        result = import_module_from_str("django.urls")
        self.assertTrue(hasattr(result, "reverse"))
        self.assertTrue(callable(result.reverse))

    def test_import_single_module(self):
        # Test importing a single module like "django"
        result = import_module_from_str("django")
        self.assertTrue(hasattr(result, "setup"))
        self.assertTrue(callable(result.setup))

    def test_invalid_import(self):
        # Test that invalid imports raise an exception
        with self.assertRaises(Exception) as context:
            import_module_from_str("nonexistent.module")

        self.assertIn("No module named", str(context.exception))

    def test_import_nested_attribute(self):
        # Test importing and accessing nested attributes
        result = import_module_from_str("django.contrib")
        self.assertTrue(hasattr(result, "admin"))
        self.assertTrue(hasattr(result.admin, "sites"))
