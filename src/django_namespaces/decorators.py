from functools import wraps

from django.http import HttpResponse
from django.template import loader

from django_namespaces.conf import settings
from django_namespaces.middleware import AnonymousNamespace


def namespace_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, "namespace"):
            template = loader.get_template(
                settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
            )
            return HttpResponse(template.render({}, request))
        if not request.namespace:
            template = loader.get_template(
                settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
            )
            return HttpResponse(template.render({}, request))
        if isinstance(request.namespace, AnonymousNamespace):
            template = loader.get_template(
                settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
            )
            return HttpResponse(template.render({}, request))
        return view_func(request, *args, **kwargs)

    return _wrapped_view
