from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase

from django_namespaces.utils import CACHE_KEY_PREFIX
from django_namespaces.utils import get_or_set_cached_user_namespaces
from django_namespaces.utils import set_user_cached_namespaces


class NamespaceUtilsTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Clear cache before each test
        cache.clear()

    def test_set_user_cached_namespaces(self):
        # Test setting namespaces in cache
        namespaces = set_user_cached_namespaces(self.user)

        # Verify cache was set
        cache_key = f"{CACHE_KEY_PREFIX}_{self.user.id}"
        cached_namespaces = cache.get(cache_key)

        # Convert QuerySets to lists for comparison
        self.assertEqual(list(namespaces), list(cached_namespaces))

    def test_get_or_set_cached_user_namespaces_with_empty_cache(self):
        # Test getting namespaces when cache is empty
        namespaces = get_or_set_cached_user_namespaces(self.user)

        # Verify cache was set
        cache_key = f"{CACHE_KEY_PREFIX}_{self.user.id}"
        cached_namespaces = cache.get(cache_key)

        self.assertIsNotNone(cached_namespaces)
        self.assertEqual(list(namespaces), list(cached_namespaces))

    def test_get_or_set_cached_user_namespaces_with_populated_cache(self):
        # First, set the cache
        initial_namespaces = set_user_cached_namespaces(self.user)

        # Then try to get the cached namespaces
        cached_namespaces = get_or_set_cached_user_namespaces(self.user)

        self.assertEqual(list(initial_namespaces), list(cached_namespaces))

    def tearDown(self):
        # Clean up cache after each test
        cache.clear()
