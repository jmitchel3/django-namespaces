from __future__ import annotations

from django.test import TestCase

from django_namespaces.blocked import blocked_namespaces


class BlockedNamespacesTestCase(TestCase):
    def test_blocked_namespaces_list_exists(self):
        """Test that the blocked namespaces list exists and is not empty"""
        self.assertTrue(len(blocked_namespaces) > 0)

    def test_common_blocked_namespaces(self):
        """Test that common sensitive namespaces are blocked"""
        important_blocked = [
            "admin",
            "login",
            "logout",
            "api",
            "settings",
            "profile",
            "auth",
        ]
        for namespace in important_blocked:
            self.assertIn(namespace, blocked_namespaces)

    def test_blocked_namespaces_are_strings(self):
        """Test that all blocked namespaces are strings"""
        for namespace in blocked_namespaces:
            self.assertIsInstance(namespace, str)

    def test_blocked_namespaces_are_lowercase(self):
        """Test that all blocked namespaces are lowercase"""
        for namespace in blocked_namespaces:
            self.assertEqual(namespace.lower(), namespace)

    def test_no_duplicate_namespaces(self):
        """Test that there are no duplicate namespaces in the list"""
        unique_namespaces = set(blocked_namespaces)
        self.assertEqual(len(blocked_namespaces), len(unique_namespaces))

    def test_no_empty_namespaces(self):
        """Test that there are no empty strings in the blocked list"""
        for namespace in blocked_namespaces:
            self.assertTrue(len(namespace) > 0)
