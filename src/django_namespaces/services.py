from __future__ import annotations

import swapper
from django.core.cache import cache
from django.db.models import QuerySet

from django_namespaces.conf import settings
from django_namespaces.validators import validate_lookup_expression

CACHE_SECONDS = settings.DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS
CACHE_KEY_PREFIX = settings.DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX
DJANGO_NAMESPACES_USER_LOOKUP_EXPRESSION = (
    settings.DJANGO_NAMESPACES_USER_LOOKUP_EXPRESSION
)


def get_cache_key(user=None):
    prefix = CACHE_KEY_PREFIX
    prefix = prefix.rstrip(":")
    if user is None:
        return f"{prefix}"
    return f"{prefix}:{user.id}"


def get_namespaces(
    user=None,
    use_caching=True,
    refresh_cache=False,
    user_lookup_expression=DJANGO_NAMESPACES_USER_LOOKUP_EXPRESSION,
) -> QuerySet | list:
    NamespaceModel = swapper.load_model("django_namespaces", "Namespace")
    lookups = {}
    if all(
        [
            user is not None,
            "user" in [x.name for x in NamespaceModel._meta.get_fields()],
            user_lookup_expression is None,
        ]
    ):
        lookups["user"] = user
    elif all([user is not None, isinstance(user_lookup_expression, str)]):
        if validate_lookup_expression(NamespaceModel, user_lookup_expression):
            lookups[user_lookup_expression] = user

    cache_key = get_cache_key(user)

    # Only check cache if use_caching is True and not refreshing
    if use_caching and not refresh_cache:
        qs = cache.get(cache_key)
        if qs is not None:
            return qs

    if len(lookups) > 0:
        qs = NamespaceModel.objects.filter(**lookups)
    else:
        qs = NamespaceModel.objects.none()
    if not use_caching:
        # Always evaluate the queryset when not using cache
        return list(qs)

    # Only cache if use_caching is True or explicitly refreshing
    if use_caching or refresh_cache:
        cache.set(cache_key, qs, CACHE_SECONDS)

    return qs
