from __future__ import annotations

from functools import lru_cache

from django.conf import settings as django_settings


class Settings:
    """
    Shadow Django's settings with a little logic
    """
    @property
    def DJANGO_NAMESPACE_MODEL(self) -> str:
        return getattr(django_settings, "DEFAULT_NAMESPACE_MODEL", "django_namespaces.models.Namespace")
    
    @property
    def DJANGO_NAMESPACE_BLOCKED_LIST(self) -> int:
        return getattr(django_settings, "DJANGO_NAMESPACE_BLOCKED_LIST", "django_namespaces.blocked.blocked_namespaces")
    
    @property
    def DJANGO_NAMESPACE_MAX_SLUG_LENGTH(self) -> str:
        return getattr(django_settings, "DJANGO_NAMESPACE_MAX_SLUG_LENGTH", 50)

    @property
    def DJANGO_NAMESPACE_CREATE_FORM(self) -> str:
        return getattr(django_settings, "DEFAULT_NAMESPACE_MODEL", "django_namespaces.forms.NamespaceCreateForm")

    @property
    def DJANGO_NAMESPACE_UPDATE_FORM(self) -> str:
        return getattr(django_settings, "DEFAULT_NAMESPACE_MODEL", "django_namespaces.forms.NamespaceUpdateForm")

    @property
    def DJANGO_NAMESPACE_URL_REVERSE_FUNCTION(self) -> str:
        return getattr(django_settings, "DJANGO_NAMESPACE_URL_REVERSE_FUNCTION", "django.urls.reverse")
    
    @property
    def DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL(self) -> str:
        return getattr(django_settings, "DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL", "/")

@lru_cache
def get_settings() -> Settings:
    return Settings()



settings = get_settings()