from __future__ import annotations

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory
from django.test import TestCase

from django_namespaces.middleware import AnonymousNamespace
from django_namespaces.middleware import NamespaceDetails
from django_namespaces.middleware import NamespaceMiddleware


class NamespaceMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def get_response(self, request):
        return HttpResponse("Test response")

    def test_middleware_without_namespace(self):
        request = self.factory.get("/")
        request.session = {}

        middleware = NamespaceMiddleware(self.get_response)
        middleware(request)

        self.assertTrue(hasattr(request, "namespace"))
        self.assertIsInstance(request.namespace, AnonymousNamespace)
        self.assertIsNone(request.namespace.value)
        self.assertIsNone(request.namespace.handle)

    def test_middleware_with_namespace(self):
        request = self.factory.get("/")
        request.session = {"namespace": "test-namespace", "namespace_id": "123"}

        middleware = NamespaceMiddleware(self.get_response)
        middleware(request)

        self.assertTrue(hasattr(request, "namespace"))
        self.assertIsInstance(request.namespace, NamespaceDetails)
        self.assertEqual(request.namespace.value, "test-namespace")
        self.assertEqual(request.namespace.handle, "test-namespace")
        self.assertEqual(request.namespace.id, "123")
        self.assertTrue(request.namespace.has_namespace)

    def test_namespace_details_repr(self):
        request = self.factory.get("/")
        request.session = {"namespace": "test-namespace"}

        namespace = NamespaceDetails(request)
        self.assertEqual(repr(namespace), "<Namespace test-namespace>")
        self.assertEqual(str(namespace), "test-namespace")

    async def test_async_middleware(self):
        request = self.factory.get("/")
        request.session = {"namespace": "async-namespace"}

        async def async_get_response(request):
            return HttpResponse("Async response")

        middleware = NamespaceMiddleware(async_get_response)
        await middleware(request)

        self.assertTrue(hasattr(request, "namespace"))
        self.assertIsInstance(request.namespace, NamespaceDetails)
        self.assertEqual(request.namespace.value, "async-namespace")
