from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase

from django_namespaces.forms import NamespaceCreateForm
from django_namespaces.forms import NamespaceUpdateForm
from django_namespaces.models import Namespace

User = get_user_model()


class NamespaceFormsTest(TestCase):
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

    def test_namespace_create_form_valid(self):
        form_data = {
            "handle": "new-namespace",
        }
        form = NamespaceCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_namespace_create_form_invalid(self):
        # Test with invalid slug characters
        form_data = {
            "handle": "invalid namespace!",
        }
        form = NamespaceCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("handle", form.errors)

    def test_namespace_update_form_valid(self):
        form_data = {
            "handle": "updated-namespace",
            "title": "Updated Title",
            "description": "Updated description",
        }
        form = NamespaceUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_namespace_update_form_invalid(self):
        # Test with invalid slug characters
        form_data = {
            "handle": "invalid namespace!",
            "title": "Updated Title",
            "description": "Updated description",
        }
        form = NamespaceUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("handle", form.errors)

    def test_namespace_update_form_empty_optional_fields(self):
        form_data = {
            "handle": "valid-namespace",
            "title": "",
            "description": "",
        }
        form = NamespaceUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
