from __future__ import annotations

from functools import lru_cache

from django.conf import settings as django_settings


class Settings:
    """
    Shadow Django's settings with a little logic
    """
    @property
    def DJANGO_NAMESPACE_MODEL(self) -> str:
        """
        Tge default model to use for namespaces
        """
        return getattr(django_settings, "DEFAULT_NAMESPACE_MODEL", "django_namespaces.models.Namespace")
    
    @property
    def DJANGO_NAMESPACE_BLOCKED_LIST(self) -> int:
        """
        A list of namespaces that are not allowed to be created
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_BLOCKED_LIST", "django_namespaces.blocked.blocked_namespaces")
    
    @property
    def DJANGO_NAMESPACE_MAX_SLUG_LENGTH(self) -> str:
        """
        The max length of a namespace slug
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_MAX_SLUG_LENGTH", 50)

    @property
    def DJANGO_NAMESPACE_CREATE_FORM(self) -> str:
        """
        The form to use for creating a namespace 
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_CREATE_FORM", "django_namespaces.forms.NamespaceCreateForm")

    @property
    def DJANGO_NAMESPACE_UPDATE_FORM(self) -> str:
        """
        The form to use for updating a namespace
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_UPDATE_FORM", "django_namespaces.forms.NamespaceUpdateForm")

    @property
    def DJANGO_NAMESPACE_URL_REVERSE_FUNCTION(self) -> str:
        """
        The function to use for reversing urls
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_URL_REVERSE_FUNCTION", "django.urls.reverse")
    
    @property
    def DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL(self) -> str:
        """
        The url to redirect to after activating a namespace
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL", "/")

    @property
    def DJANGO_NAMESPACE_CONTEXT_PROCESSOR_CACHE_SECONDS(self) -> int:
        """
        Duration to cache the context processor in Seconds
        Default is 1 hour
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_CONTEXT_PROCESSOR_CACHE_SECONDS", 3600)
    
    @property
    def DJANGO_NAMESPACE_CONTEXT_PROCESSOR_CACHE_KEY_PREFIX(self) -> str:
        """
        The prefix to use for the cache key for the context processor
        """
        return getattr(django_settings, "DJANGO_NAMESPACE_CONTEXT_PROCESSOR_CACHE_KEY_PREFIX", "django_ns_cp_")

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
