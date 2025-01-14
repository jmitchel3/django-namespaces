from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory
from django.test import TestCase
from django.views import View

from django_namespaces.conf import settings
from django_namespaces.decorators import namespace_required
from django_namespaces.middleware import AnonymousNamespace
from django_namespaces.middleware import NamespaceDetails
from django_namespaces.mixins import NamespaceRequiredMixin


class NamespaceDecoratorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_view_with_valid_namespace(self):
        @namespace_required
        def test_view(request):
            return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {"namespace": "test-namespace"}
        request.namespace = NamespaceDetails(request)

        response = test_view(request)
        self.assertEqual(response.content.decode(), "Success")

    @patch("django.template.loader.get_template")
    def test_view_without_namespace_attribute(self, mock_get_template):
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "Please activate namespace"

        @namespace_required
        def test_view(request):
            return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {}

        response = test_view(request)

        mock_get_template.assert_called_once_with(
            settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
        )
        mock_template.render.assert_called_once_with({}, request)
        self.assertEqual(response.content.decode(), "Please activate namespace")

    @patch("django.template.loader.get_template")
    def test_view_with_none_namespace(self, mock_get_template):
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "Please activate namespace"

        @namespace_required
        def test_view(request):
            return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {}
        request.namespace = None

        response = test_view(request)

        mock_get_template.assert_called_once_with(
            settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
        )
        mock_template.render.assert_called_once_with({}, request)
        self.assertEqual(response.content.decode(), "Please activate namespace")

    @patch("django.template.loader.get_template")
    def test_view_with_anonymous_namespace(self, mock_get_template):
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "Please activate namespace"

        @namespace_required
        def test_view(request):
            return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {}
        request.namespace = AnonymousNamespace()

        response = test_view(request)

        mock_get_template.assert_called_once_with(
            settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
        )
        mock_template.render.assert_called_once_with({}, request)
        self.assertEqual(response.content.decode(), "Please activate namespace")


class NamespaceMixinTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_view_with_valid_namespace(self):
        class TestView(NamespaceRequiredMixin, View):
            def get(self, request):
                return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {"namespace": "test-namespace"}
        request.namespace = NamespaceDetails(request)

        view = TestView.as_view()
        response = view(request)
        self.assertEqual(response.content.decode(), "Success")

    @patch("django.template.loader.get_template")
    def test_view_without_namespace_attribute(self, mock_get_template):
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "Please activate namespace"

        class TestView(NamespaceRequiredMixin, View):
            def get(self, request):
                return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {}

        view = TestView.as_view()
        response = view(request)

        mock_get_template.assert_called_once_with(
            settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
        )
        mock_template.render.assert_called_once_with({}, request)
        self.assertEqual(response.content.decode(), "Please activate namespace")

    @patch("django.template.loader.get_template")
    def test_view_with_none_namespace(self, mock_get_template):
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "Please activate namespace"

        class TestView(NamespaceRequiredMixin, View):
            def get(self, request):
                return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {}
        request.namespace = None

        view = TestView.as_view()
        response = view(request)

        mock_get_template.assert_called_once_with(
            settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
        )
        mock_template.render.assert_called_once_with({}, request)
        self.assertEqual(response.content.decode(), "Please activate namespace")

    @patch("django.template.loader.get_template")
    def test_view_with_anonymous_namespace(self, mock_get_template):
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "Please activate namespace"

        class TestView(NamespaceRequiredMixin, View):
            def get(self, request):
                return HttpResponse("Success")

        request = self.factory.get("/")
        request.session = {}
        request.namespace = AnonymousNamespace()

        view = TestView.as_view()
        response = view(request)

        mock_get_template.assert_called_once_with(
            settings.DJANGO_NAMESPACE_NEEDS_ACTIVATION_TEMPLATE
        )
        mock_template.render.assert_called_once_with({}, request)
        self.assertEqual(response.content.decode(), "Please activate namespace")
