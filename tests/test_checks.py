from __future__ import annotations

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.test import TestCase

from django_namespaces.checks import check_namespace_model


class NamespaceChecksTests(TestCase):
    def test_valid_namespace_model(self):
        """Test that a valid namespace model passes all checks."""
        with override_settings(
            DJANGO_NAMESPACES_NAMESPACE_MODEL="test_app.ValidNamespaceModel"
        ):
            errors = check_namespace_model(None)
            self.assertEqual(errors, [])

    def test_missing_model(self):
        """Test that an invalid model path raises an error."""
        with self.assertRaises(ImproperlyConfigured):
            with override_settings(
                DJANGO_NAMESPACES_NAMESPACE_MODEL="test_app.NonExistentModel"
            ):
                check_namespace_model(None)

    def test_missing_required_field(self):
        """Test that a model missing required fields raises an error."""
        with override_settings(
            DJANGO_NAMESPACES_NAMESPACE_MODEL="test_app.InvalidNamespaceModel"
        ):
            errors = check_namespace_model(None)
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0].id, "django_namespaces.E003")

    def test_wrong_field_type(self):
        """Test that a model with wrong field type raises an error."""
        with override_settings(
            DJANGO_NAMESPACES_NAMESPACE_MODEL="test_app.WrongFieldTypeNamespaceModel"
        ):
            errors = check_namespace_model(None)
            error_ids = [error.id for error in errors]
            self.assertIn("django_namespaces.E002", error_ids)
            # We expect E002 for wrong field type and E004 for non-unique field
            self.assertEqual(len(errors), 2)

    def test_non_unique_handle(self):
        """Test that a model with non-unique handle raises an error."""
        with override_settings(
            DJANGO_NAMESPACES_NAMESPACE_MODEL="test_app.NonUniqueHandleNamespaceModel"
        ):
            errors = check_namespace_model(None)
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0].id, "django_namespaces.E004")
