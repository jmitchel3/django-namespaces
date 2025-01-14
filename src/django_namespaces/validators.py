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
    # Check for invalid characters
    if not value.replace("-", "").isalnum():
        raise ValidationError(
            _("Namespace can only contain letters, numbers, and hyphens.")
        )

    # Check length (assuming reasonable min/max values)
    if len(value) < 2:
        raise ValidationError(_("Namespace must be at least 2 characters long."))
    if len(value) > 63:  # Common DNS label length limit
        raise ValidationError(_("Namespace cannot be longer than 63 characters."))

    # Check blocked list (existing code)
    blocked_list = get_blocked_list(as_slugs=False)
    blocked_list_as_slugs = get_blocked_list(as_slugs=True)
    if value in blocked_list:
        raise ValidationError(_(f"{value} is not allowed as a namespace."))
    if value in blocked_list_as_slugs:
        raise ValidationError(_(f"{value} is not a valid namespace."))
