from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from django_namespaces.conf import settings
from django_namespaces.models import Namespace

PROJECT_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = PROJECT_DIR / "tests"
FIXTURES_DIR = TESTS_DIR / "fixtures"
NAMESPACES_FIXTURE = FIXTURES_DIR / "namespaces" / "test_namespaces.json"

User = get_user_model()


class BaseNamespaceTest(TestCase):
    fixtures = [f"{NAMESPACES_FIXTURE}"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Force database to be recreated
        from django.db import connection

        connection.close()

    def setUp(self):
        self.user = User.objects.all().first()
        self.namespace = Namespace.objects.get(handle="winterfell")
        self.user.set_password("testpass123")
        self.user.save()
        self.client.login(username="admin", password="testpass123")


class NamespaceListViewTest(BaseNamespaceTest):
    def test_namespace_list_view(self):
        response = self.client.get(reverse("django_namespaces:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_list.html")

        self.assertIn("object_list", response.context)
        request_object_list = response.context["object_list"]
        request_object_list = sorted([x.handle for x in request_object_list])
        self.assertIn(
            self.namespace.handle,
            request_object_list,
        )

        self.assertContains(response, f"View {self.namespace.handle}")

    def test_htmx_list_view(self):
        response = self.client.get(
            reverse("django_namespaces:list"), HTTP_HX_REQUEST="true"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "django_namespaces/snippets/namespace_list.html"
        )

        response = self.client.get(reverse("django_namespaces:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_list.html")


class NamespaceCreateViewTest(BaseNamespaceTest):
    def test_namespace_create_view(self):
        response = self.client.get(reverse("django_namespaces:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_create.html")

        response = self.client.post(
            reverse("django_namespaces:create"),
            {"handle": "new-namespace"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Namespace.objects.filter(handle="new-namespace").exists())

    def test_namespace_create_view_invalid_data(self):
        response = self.client.post(
            reverse("django_namespaces:create"),
            {"handle": ""},  # Invalid empty handle
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Namespace.objects.filter(handle="").exists())

    def test_htmx_create_view(self):
        response = self.client.get(
            reverse("django_namespaces:create"),
            HTTP_HX_REQUEST="true",
        )
        self.assertTemplateUsed(
            response, "django_namespaces/snippets/namespace_create.html"
        )


class NamespaceDetailUpdateViewTest(BaseNamespaceTest):
    def setUp(self):
        super().setUp()
        # Create a test-specific namespace for each test
        self.test_namespace = Namespace.objects.create(
            handle="test-namespace",
            title="Test Title",
            description="Test Description",
            user=self.user,
        )

    def test_namespace_detail_update_view(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.test_namespace.handle},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_update.html")

        response = self.client.post(
            url,
            {
                "handle": "updated-namespace",
                "title": "Updated Title",
                "description": "Updated description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.test_namespace.refresh_from_db()
        self.assertEqual(self.test_namespace.handle, "updated-namespace")
        self.assertEqual(self.test_namespace.title, "Updated Title")

    def test_namespace_detail_update_view_invalid_data(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.test_namespace.handle},
        )
        response = self.client.post(
            url,
            {
                "handle": "",
                "title": "Updated Title",
                "description": "Updated description",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.test_namespace.refresh_from_db()
        self.assertEqual(self.test_namespace.handle, "test-namespace")

    def test_namespace_detail_context(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.test_namespace.handle},
        )
        response = self.client.get(url)
        self.assertIn("activated", response.context)
        self.assertIsInstance(response.context["activated"], bool)


class NamespaceDeleteViewTest(BaseNamespaceTest):
    def test_namespace_delete_view(self):
        url = reverse(
            "django_namespaces:delete", kwargs={"handle": self.namespace.handle}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_delete.html")

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Namespace.objects.filter(handle=self.namespace.handle).exists()
        )


class NamespaceActivationViewTest(BaseNamespaceTest):
    def test_namespace_activation_view(self):
        url = reverse(
            "django_namespaces:activate", kwargs={"handle": self.namespace.handle}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_namespace_activation_with_htmx(self):
        url = reverse(
            "django_namespaces:activate", kwargs={"handle": self.namespace.handle}
        )
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")

        response = self.client.get(url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"{self.namespace.handle} activated.")
        self.assertEqual(
            response.redirect_chain[0][0],
            settings.DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL,
        )


class NamespaceUnauthorizedAccessTest(BaseNamespaceTest):
    def setUp(self):
        super().setUp()
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.other_namespace = Namespace.objects.create(
            handle="other-namespace", user=self.other_user
        )

    def test_unauthorized_access(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.other_namespace.handle},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_namespace_delete_view_unauthorized(self):
        url = reverse(
            "django_namespaces:delete", kwargs={"handle": self.other_namespace.handle}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Namespace.objects.filter(handle=self.other_namespace.handle).exists()
        )

    def test_namespace_activation_view_unauthorized(self):
        url = reverse(
            "django_namespaces:activate", kwargs={"handle": self.other_namespace.handle}
        )
        for method in [self.client.get, self.client.post]:
            response = method(url)
            self.assertEqual(
                response.status_code,
                404,
                f"Expected 404 for {method.__name__}, got {response.status_code}",
            )


class NamespaceMessagesTest(BaseNamespaceTest):
    def setUp(self):
        super().setUp()
        # Remove the manual namespace creation since it's in the fixtures
        pass

    def test_create_success_message(self):
        new_handle = "message-test"
        response = self.client.post(
            reverse("django_namespaces:create"), {"handle": new_handle}, follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"{new_handle} was created successfully.")

    def test_update_success_message(self):
        updated_handle = "message-test-updated"
        response = self.client.post(
            reverse(
                "django_namespaces:detail-update",
                kwargs={"handle": self.namespace.handle},
            ),
            {
                "handle": updated_handle,
                "title": "Updated Title",
                "description": "Updated description",
            },
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"{updated_handle} was updated.")

    def test_delete_success_message(self):
        response = self.client.post(
            reverse(
                "django_namespaces:delete", kwargs={"handle": self.namespace.handle}
            ),
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Namespace was deleted successfully.")


class NamespaceClearViewTest(BaseNamespaceTest):
    def test_clear_namespaces_view(self):
        response = self.client.get(reverse("django_namespaces:clear"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("django_namespaces:list"))

        response = self.client.post(reverse("django_namespaces:clear"), follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "All namespaces deactivated.")
