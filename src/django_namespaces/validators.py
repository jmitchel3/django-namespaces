from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext as _

from django_namespaces.conf import settings as django_namespace_settings
from django_namespaces.import_utils import import_module_from_str

DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION = (
    django_namespace_settings.DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION
)


def get_blocked_list(as_slugs: bool = False) -> list[str]:
    blocked_items = import_module_from_str(DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION)
    if isinstance(blocked_items, list):
        if as_slugs:
            return [slugify(x) for x in blocked_items]
        return blocked_items
    raise ValueError(
        f"The blocked list at {DJANGO_NAMESPACES_BLOCKED_LIST_LOCATION} is not a list"
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


def validate_lookup_expression(model, lookup_expression: str) -> bool:
    """
    Validates if a lookup expression is valid for a given model.

    Args:
        model: Django model class
        lookup_expression: String representing the lookup path (e.g., 'user__group__name')

    Returns:
        bool: True if valid

    Raises:
        ValueError: If the lookup expression is invalid
    """
    model_dot_path = f"{model._meta.app_label}.models.{model.__name__}"
    try:
        parts = lookup_expression.split("__")
        current_model = model

        for part in parts:
            field = current_model._meta.get_field(part)
            if hasattr(field, "remote_field") and field.remote_field:
                current_model = field.remote_field.model
        return True
    except Exception as e:
        msg = f"""Error with `settings.DJANGO_NAMESPACES_USER_LOOKUP_EXPRESSION='{lookup_expression}'`.
The model `{model_dot_path}` cannot be queried with this expression. {e}"""
        raise ValueError(msg)
