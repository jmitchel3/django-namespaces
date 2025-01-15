from __future__ import annotations

import swapper
from django.core.cache import cache

from django_namespaces.conf import settings

CACHE_SECONDS = settings.DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS
CACHE_KEY_PREFIX = settings.DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX


def get_cache_key(user=None):
    prefix = CACHE_KEY_PREFIX
    prefix = prefix.rstrip(":")
    if user is None:
        return f"{prefix}"
    return f"{prefix}:{user.id}"


def get_namespaces(user=None, use_caching=True, refresh_cache=False):
    NamespaceModel = swapper.load_model("django_namespaces", "Namespace")
    lookups = {}
    if "user" in NamespaceModel._meta.fields:
        lookups["user"] = user

    cache_key = get_cache_key(user)

    # Only check cache if use_caching is True and not refreshing
    if use_caching and not refresh_cache:
        qs = cache.get(cache_key)
        if qs is not None:
            return qs

    # Always evaluate the queryset when not using cache
    if len(lookups) > 0:
        qs = list(NamespaceModel.objects.filter(**lookups))
    else:
        qs = list(NamespaceModel.objects.all())

    # Only cache if use_caching is True or explicitly refreshing
    if use_caching or refresh_cache:
        cache.set(cache_key, qs, CACHE_SECONDS)

    return qs
