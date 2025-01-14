from __future__ import annotations

from django_namespaces import services


def user_namespaces(request):
    if request.user.is_authenticated:
        return {"user_namespaces": services.get_namespaces(request.user)}
    return {}
