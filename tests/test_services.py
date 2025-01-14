from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
from django.test import TestCase

from django_namespaces.models import Namespace
from django_namespaces.services import CACHE_KEY_PREFIX
from django_namespaces.services import get_cache_key
from django_namespaces.services import get_namespaces


class NamespaceUtilsTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.namespace = Namespace.objects.create(
            user=self.user, handle="testnamespace"
        )
        # Clear cache before each test
        cache.clear()

    def tearDown(self):
        # Clean up cache after each test
        cache.clear()

    def test_get_cache_key(self):
        """Test cache key generation"""
        # Test with user
        key = f"{CACHE_KEY_PREFIX}".rstrip(":")
        expected_key = f"{key}:{self.user.id}"
        self.assertEqual(get_cache_key(self.user), expected_key)

        # Test without user
        expected_key = CACHE_KEY_PREFIX.rstrip(":")
        self.assertEqual(get_cache_key(), expected_key)

    def test_get_namespaces_caching(self):
        """Test that get_namespaces properly caches and retrieves from cache"""
        # First call should hit the database and cache the result
        namespaces = get_namespaces(self.user)

        # Second call should retrieve from cache
        with connection.execute_wrapper(lambda x: self.fail("Database was queried")):
            cached_namespaces = get_namespaces(self.user)

        self.assertEqual(list(namespaces), list(cached_namespaces))

    def test_get_namespaces_refresh_cache(self):
        """Test that refresh_cache forces a new database query"""
        # Initial call to cache namespaces
        initial_namespaces = get_namespaces(self.user)

        # Force refresh should hit database again
        with self.assertNumQueries(1):
            refreshed_namespaces = get_namespaces(self.user, refresh_cache=True)

        self.assertEqual(list(initial_namespaces), list(refreshed_namespaces))

    def test_get_namespaces_no_cache(self):
        """Test that use_caching=False bypasses cache"""
        # Should hit database each time when use_caching is False
        with self.assertNumQueries(1):
            namespaces1 = get_namespaces(
                self.user, use_caching=False, refresh_cache=False
            )

        with self.assertNumQueries(1):
            namespaces2 = get_namespaces(
                self.user, use_caching=False, refresh_cache=False
            )

        self.assertEqual(list(namespaces1), list(namespaces2))
