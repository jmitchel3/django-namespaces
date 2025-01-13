from django.core.cache import cache

from django_namespaces.conf import settings as django_namespaces_settings
from django_namespaces.import_utils import import_module_from_str

CACHE_SECONDS = (
    django_namespaces_settings.DJANGO_NAMESPACE_CONTEXT_PROCESSOR_CACHE_SECONDS
)
CACHE_KEY_PREFIX = (
    django_namespaces_settings.DJANGO_NAMESPACE_CONTEXT_PROCESSOR_CACHE_KEY_PREFIX
)


def set_user_cached_namespaces(user):
    cache_key = f"{CACHE_KEY_PREFIX}_{user.id}"
    NamespaceModel = import_module_from_str(
        django_namespaces_settings.DJANGO_NAMESPACE_MODEL
    )
    user_namespaces = NamespaceModel.objects.filter(user=user)
    cache.set(cache_key, user_namespaces, CACHE_SECONDS)
    return user_namespaces


def get_or_set_cached_user_namespaces(user):
    cache_key = f"{CACHE_KEY_PREFIX}_{user.id}"
    cached_user_namespaces = cache.get(cache_key)
    if cached_user_namespaces:
        return cached_user_namespaces
    return set_user_cached_namespaces(user)
