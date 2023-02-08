from django.http import HttpResponse

import django_namespaces


def namespace_view(request):
    if not request.has_namespace:
        return HttpResponse("No namespace is set")
    return HttpResponse(f"{request.namespace}")


def namespace_set_view(request, namespace=None):
    django_namespaces.activate(request, namespace=namespace)
    return HttpResponse(f"{request.namespace}")



def clear_namespace(request):
    django_namespaces.clear(request)
    return HttpResponse(f"{request.namespace}")