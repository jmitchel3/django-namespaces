from __future__ import annotations

import swapper
from django.conf import settings
from django.core import checks
from django.core.exceptions import FieldDoesNotExist


@checks.register("django_namespaces")
def check_namespace_model(app_configs, **kwargs):
    """
    System check to validate that the swapped Namespace model contains
    all required fields from AbstractNamespace.
    """
    errors = []

    # Get the swapped model class
    try:
        swapped_model = swapper.load_model("django_namespaces", "Namespace")
    except (ValueError, LookupError):
        errors.append(
            checks.Error(
                f"Could not find swapped model: {settings.DJANGO_NAMESPACES_NAMESPACE_MODEL}",
                id="django_namespaces.E001",
            )
        )
        return errors

    # Define required fields and their types
    required_fields = {
        "handle": "SlugField",
    }

    # Check each required field
    for field_name, field_type in required_fields.items():
        try:
            field = swapped_model._meta.get_field(field_name)
            if not field.__class__.__name__ == field_type:
                errors.append(
                    checks.Error(
                        f"Field '{field_name}' in {swapped_model.__name__} must be a {field_type}",
                        id="django_namespaces.E002",
                        obj=swapped_model,
                    )
                )
        except FieldDoesNotExist:
            errors.append(
                checks.Error(
                    f"Required field '{field_name}' is missing in {swapped_model.__name__}",
                    id="django_namespaces.E003",
                    obj=swapped_model,
                )
            )

    # Check specific field attributes
    try:
        handle_field = swapped_model._meta.get_field("handle")
        if not handle_field.unique:
            errors.append(
                checks.Error(
                    f"Field 'handle' in {swapped_model.__name__} must be unique",
                    id="django_namespaces.E004",
                    obj=swapped_model,
                )
            )
    except FieldDoesNotExist:
        pass  # Already handled in the field existence check

    # Check required methods
    # required_methods = [
    #     "get_absolute_url",
    #     "get_activation_url",
    #     "get_delete_url",
    #     "namespace",
    # ]

    # for method_name in required_methods:
    #     if not hasattr(swapped_model, method_name):
    #         errors.append(
    #             checks.Error(
    #                 f"Required method '{method_name}' is missing in {swapped_model.__name__}",
    #                 id="django_namespaces.E005",
    #                 obj=swapped_model,
    #             )
    #         )

    return errors
