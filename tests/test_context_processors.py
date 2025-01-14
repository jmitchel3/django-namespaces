from __future__ import annotations

import unittest.mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.test import TestCase

from django_namespaces import context_processors
from django_namespaces import utils


class ContextProcessorsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_user_namespaces_authenticated(self):
        """Test that user_namespaces returns correct context for authenticated users"""
        request = self.factory.get("/")
        request.user = self.user

        # Mock the cache function to return test data
        test_namespaces = ["namespace1", "namespace2"]
        with unittest.mock.patch.object(
            utils, "get_or_set_cached_user_namespaces", return_value=test_namespaces
        ):
            context = context_processors.user_namespaces(request)

            self.assertIn("user_namespaces", context)
            self.assertEqual(context["user_namespaces"], test_namespaces)

    def test_user_namespaces_unauthenticated(self):
        """Test that user_namespaces returns empty context for unauthenticated users"""
        request = self.factory.get("/")
        request.user = AnonymousUser()

        context = context_processors.user_namespaces(request)

        self.assertEqual(context, {})
