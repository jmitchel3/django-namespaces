from __future__ import annotations

from functools import lru_cache

from django.conf import settings as django_settings


class Settings:
    """
    Shadow Django's settings with a little logic
    """

    @property
    def DJANGO_NAMESPACES_NAMESPACE_MODEL(self) -> str:
        """
        The model to use for namespaces
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_NAMESPACE_MODEL",
            "django_namespaces.Namespace",
        )

    @property
    def DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION(self) -> str:
        """
        Dot notation for the location of the list of namespaces
        that are not allowed to be created.
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION",
            "django_namespaces.blocked.blocked_namespaces",
        )

    @property
    def DJANGO_NAMESPACES_NEEDS_ACTIVATION_TEMPLATE(self) -> str:
        """
        The template to use when a namespace is not activated
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_NEEDS_ACTIVATION_TEMPLATE",
            "django_namespaces/namespace_needs_activation.html",
        )

    @property
    def DJANGO_NAMESPACES_MAX_HANDLE_LENGTH(self) -> int:
        """
        The max length of a namespace handle
        """
        return getattr(django_settings, "DJANGO_NAMESPACES_MAX_HANDLE_LENGTH", 50)

    @property
    def DJANGO_NAMESPACES_CREATE_FORM(self) -> str:
        """
        The form to use for creating a namespace
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_CREATE_FORM",
            "django_namespaces.forms.NamespaceCreateForm",
        )

    @property
    def DJANGO_NAMESPACES_UPDATE_FORM(self) -> str:
        """
        The form to use for updating a namespace
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_UPDATE_FORM",
            "django_namespaces.forms.NamespaceUpdateForm",
        )

    @property
    def DJANGO_NAMESPACES_URL_REVERSE_FUNCTION(self) -> str:
        """
        The function to use for reversing urls
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_URL_REVERSE_FUNCTION",
            "django.urls.reverse",
        )

    @property
    def DJANGO_NAMESPACES_ACTIVATION_REDIRECT_URL(self) -> str:
        """
        The url to redirect to after activating a namespace
        """
        return getattr(
            django_settings, "DJANGO_NAMESPACES_ACTIVATION_REDIRECT_URL", "/"
        )

    @property
    def DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS(self) -> int:
        """
        Duration to cache the queryset in Seconds
        Default is 1 hour
        """
        return getattr(
            django_settings, "DJANGO_NAMESPACES_QUERYSET_CACHE_SECONDS", 3600
        )

    @property
    def DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX(self) -> str:
        """
        The prefix to use for the cache key for the queryset
        """
        return getattr(
            django_settings,
            "DJANGO_NAMESPACES_QUERYSET_CACHE_KEY_PREFIX",
            "dj:namespace:qs:",
        )

    @property
    def DJANGO_NAMESPACES_FIELDS(self) -> list[str]:
        """
        The fields to use for the namespace
        """
        return getattr(django_settings, "DJANGO_NAMESPACES_FIELDS", ["handle"])


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
