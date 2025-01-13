from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext as _

from django_namespaces.conf import settings as django_namespace_settings
from django_namespaces.import_utils import import_module_from_str

DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION = (
    django_namespace_settings.DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION
)


def get_blocked_list(as_slugs: bool = False) -> list[str]:
    blocked_items = import_module_from_str(DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION)
    if isinstance(blocked_items, list):
        if as_slugs:
            return [slugify(x) for x in blocked_items]
        return blocked_items
    raise ValueError(
        f"The blocked list at {DJANGO_NAMESPACE_BLOCKED_LIST_LOCATION} is not a list"
    )


def valid_project_id(value: str) -> None:
    blocked_list = get_blocked_list(as_slugs=False)
    blocked_list_as_slugs = get_blocked_list(as_slugs=True)
    if value in blocked_list:
        raise ValidationError(_(f"{value} is not allowed as a namespace."))
    if value in blocked_list_as_slugs:
        raise ValidationError(_(f"{value} is not a valid namespace."))
