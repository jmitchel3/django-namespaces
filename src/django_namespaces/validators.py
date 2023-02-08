import importlib

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext as _

from django_namespaces.conf import settings as django_namespace_settings
from django_namespaces.import_utils import import_module_from_str

DJANGO_NAMESPACE_BLOCKED_LIST = django_namespace_settings.DJANGO_NAMESPACE_BLOCKED_LIST

def get_blocked_list():
    return import_module_from_str(DJANGO_NAMESPACE_BLOCKED_LIST)

def valid_project_id(value):
    blocked_list = get_blocked_list()
    blocked_list_as_slugs = [slugify(x) for x in blocked_list]
    if value in blocked_list:
        raise ValidationError(_(f"{value} is not allowed as a namespace."))
    if value in blocked_list_as_slugs:
        raise ValidationError(_(f"{value} is not a valid namespace."))