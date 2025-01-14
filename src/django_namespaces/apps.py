from __future__ import annotations

from django.apps import AppConfig


class DjangoNamespacesConfig(AppConfig):
    name = "django_namespaces"
    verbose_name = "Namespace"
    verbose_name_plural = "Namespaces"

    def ready(self):
        import django_namespaces.checks  # noqa
