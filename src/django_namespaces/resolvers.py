from __future__ import annotations

from django_namespaces.conf import settings as django_namespaces_settings
from django_namespaces.import_utils import import_module_from_str


def reverse(*args, **kwargs):
    """
    Reverse a URL using the configured URL reverse function
    Defaults to django.urls.reverse
    Designed to be changed to django_hosts.reverse if needed
    """
    reverse = import_module_from_str(
        django_namespaces_settings.DJANGO_NAMESPACE_URL_REVERSE_FUNCTION
    )
    return reverse(*args, **kwargs)
