from django.contrib import admin

from django_namespaces.conf import settings as django_namespaces_settings
from django_namespaces.import_utils import import_module_from_str

Namespace = import_module_from_str(django_namespaces_settings.DJANGO_NAMESPACE_MODEL)


def user_namespaces(request):
    if request.user.is_authenticated:
        return {
            "user_namespaces": Namespace.objects.filter(user=request.user)
        }
    return {}
