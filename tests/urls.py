from __future__ import annotations

from django.http import Http404
from django.http import HttpResponse
from django.urls import include
from django.urls import path


def test_view(request):
    if request.method != "GET":
        raise Http404()
    return HttpResponse("Test view")


def test_view_http401(request):
    return HttpResponse("Unauthorized", status=401)


def test_view_that_deletes_is_enabled(request):
    del request._cors_enabled
    return HttpResponse()


urlpatterns = [
    path("", test_view),
    path("foo/", test_view),
    path("test-401/", test_view_http401),
    path("delete-is-enabled/", test_view_that_deletes_is_enabled),
    path(
        "namespaces/", include("django_namespaces.urls", namespace="django_namespaces")
    ),
]
