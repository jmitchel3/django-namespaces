from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import override_settings
from django.test import TestCase

from django_namespaces.validators import get_blocked_list
from django_namespaces.validators import valid_project_id


class ValidatorsTest(TestCase):
    @override_settings(
        DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION="tests.test_data.BLOCKED_LIST"
    )
    def test_get_blocked_list(self):
        # Test regular list retrieval
        blocked_list = get_blocked_list()
        self.assertIsInstance(blocked_list, list)
        definitely_blocked_items = ["admin", "api", "test"]
        for item in definitely_blocked_items:
            self.assertIn(item, blocked_list)

        # Test slugified list retrieval
        blocked_list_slugs = get_blocked_list(as_slugs=True)
        for item in definitely_blocked_items:
            self.assertIn(item, blocked_list_slugs)

    @override_settings(
        DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION="tests.test_data.NOT_A_LIST"
    )
    def test_get_blocked_list_invalid_type(self):
        blocked_list = get_blocked_list()
        self.assertIsInstance(blocked_list, list)
        self.assertGreater(
            len(blocked_list), 0
        )  # Should contain the default blocked items

    @override_settings(
        DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION="tests.test_data.BLOCKED_LIST"
    )
    def test_valid_project_id(self):
        # Test valid project id
        valid_project_id("valid-namespace")  # Should not raise

        # Test invalid project id (in blocked list)
        with self.assertRaises(ValidationError):
            valid_project_id("admin")

        # Test invalid project id (matches slug in blocked list)
        with self.assertRaises(ValidationError):
            valid_project_id("test")

    def test_valid_project_id_invalid_characters(self):
        # Test invalid characters
        with self.assertRaises(ValidationError):
            valid_project_id("invalid!namespace")
        with self.assertRaises(ValidationError):
            valid_project_id("invalid@namespace")

    def test_valid_project_id_length(self):
        # Test too short
        with self.assertRaises(ValidationError):
            valid_project_id("a")

        # Test too long
        with self.assertRaises(ValidationError):
            valid_project_id("a" * 64)
