from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from django_namespaces.models import AnonymousNamespace
from django_namespaces.models import Namespace

User = get_user_model()


class NamespaceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.namespace = Namespace.objects.create(
            user=self.user,
            handle="test-namespace",
            title="Test Namespace",
            description="A test namespace",
        )

    def test_namespace_creation(self):
        self.assertEqual(self.namespace.handle, "test-namespace")
        self.assertEqual(self.namespace.title, "Test Namespace")
        self.assertEqual(self.namespace.description, "A test namespace")
        self.assertEqual(self.namespace.user, self.user)
        self.assertTrue(self.namespace.default)
        self.assertIsNotNone(self.namespace.created_at)
        self.assertIsNotNone(self.namespace.updated_at)

    def test_namespace_str_representation(self):
        self.assertEqual(str(self.namespace), "test-namespace")

    def test_namespace_property(self):
        self.assertEqual(self.namespace.namespace, "test-namespace")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "django_namespaces:detail-update", kwargs={"handle": "test-namespace"}
        )
        self.assertEqual(self.namespace.get_absolute_url(), expected_url)

    def test_get_activation_url(self):
        expected_url = reverse(
            "django_namespaces:activate", kwargs={"handle": "test-namespace"}
        )
        self.assertEqual(self.namespace.get_activation_url(), expected_url)

    def test_get_delete_url(self):
        expected_url = reverse(
            "django_namespaces:delete", kwargs={"handle": "test-namespace"}
        )
        self.assertEqual(self.namespace.get_delete_url(), expected_url)

    def test_default_namespace_behavior(self):
        # Create a second namespace
        namespace2 = Namespace.objects.create(
            user=self.user,
            handle="test-namespace-2",
            title="Test Namespace 2",
            default=True,
        )

        # Refresh the first namespace from db
        self.namespace.refresh_from_db()

        # The first namespace should no longer be default
        self.assertFalse(self.namespace.default)
        # The second namespace should be default
        self.assertTrue(namespace2.default)

    def test_unique_handle_constraint(self):
        # Try to create a namespace with the same handle
        with self.assertRaises(ValidationError):
            duplicate_namespace = Namespace(
                user=self.user, handle="test-namespace", title="Duplicate Namespace"
            )
            duplicate_namespace.full_clean()


class AnonymousNamespaceTest(TestCase):
    def test_anonymous_namespace(self):
        anon_namespace = AnonymousNamespace()
        self.assertIsNone(anon_namespace.handle)
