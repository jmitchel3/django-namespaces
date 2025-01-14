from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from django_namespaces.conf import settings
from django_namespaces.models import Namespace

User = get_user_model()


class NamespaceViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.namespace = Namespace.objects.create(
            user=self.user,
            handle="test-namespace",
            title="Test Namespace",
            description="A test namespace",
        )
        self.client.login(username="testuser", password="testpass123")

    def test_namespace_list_view(self):
        response = self.client.get(reverse("django_namespaces:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_list.html")
        self.assertContains(response, "test-namespace")

    def test_namespace_create_view(self):
        response = self.client.get(reverse("django_namespaces:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_create.html")

        # Test POST
        response = self.client.post(
            reverse("django_namespaces:create"),
            {"handle": "new-namespace"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Namespace.objects.filter(handle="new-namespace").exists())

    def test_namespace_detail_update_view(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.namespace.handle},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_update.html")

        # Test POST
        response = self.client.post(
            url,
            {
                "handle": "updated-namespace",
                "title": "Updated Title",
                "description": "Updated description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.namespace.refresh_from_db()
        self.assertEqual(self.namespace.handle, "updated-namespace")
        self.assertEqual(self.namespace.title, "Updated Title")

    def test_namespace_delete_view(self):
        url = reverse(
            "django_namespaces:delete", kwargs={"handle": self.namespace.handle}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "django_namespaces/namespace_delete.html")

        # Test POST (delete)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Namespace.objects.filter(handle=self.namespace.handle).exists()
        )

    def test_namespace_activation_view(self):
        url = reverse(
            "django_namespaces:activate", kwargs={"handle": self.namespace.handle}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_access(self):
        # Create another user and namespace
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        other_namespace = Namespace.objects.create(
            user=other_user,
            handle="other-namespace",
            title="Other Namespace",
        )

        # Try to access other user's namespace
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": other_namespace.handle},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_htmx_templates(self):
        # Test create view with HTMX request
        response = self.client.get(
            reverse("django_namespaces:create"),
            HTTP_HX_REQUEST="true",
        )
        self.assertTemplateUsed(
            response, "django_namespaces/snippets/namespace_create.html"
        )

        # Add test for non-HTMX request
        response = self.client.get(reverse("django_namespaces:create"))
        self.assertTemplateUsed(response, "django_namespaces/namespace_create.html")

        # Test update view with HTMX request
        response = self.client.get(
            reverse(
                "django_namespaces:detail-update",
                kwargs={"handle": self.namespace.handle},
            ),
            HTTP_HX_REQUEST="true",
        )
        self.assertTemplateUsed(
            response, "django_namespaces/snippets/namespace_update.html"
        )

    def test_namespace_create_view_invalid_data(self):
        # Test POST with invalid data
        response = self.client.post(
            reverse("django_namespaces:create"),
            {"handle": ""},  # Invalid empty handle
        )
        self.assertEqual(response.status_code, 200)  # Returns to form with errors
        self.assertFalse(Namespace.objects.filter(handle="").exists())

    def test_namespace_detail_update_view_invalid_data(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.namespace.handle},
        )
        # Test POST with invalid data
        response = self.client.post(
            url,
            {
                "handle": "",  # Invalid empty handle
                "title": "Updated Title",
                "description": "Updated description",
            },
        )
        self.assertEqual(response.status_code, 200)  # Returns to form with errors
        self.namespace.refresh_from_db()
        self.assertEqual(self.namespace.handle, "test-namespace")  # Unchanged

    def test_namespace_delete_view_unauthorized(self):
        # Create another user's namespace
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        other_namespace_object = Namespace.objects.create(
            user=other_user,
            handle="other-namespace",
        )

        # Try to delete other user's namespace
        url = reverse(
            "django_namespaces:delete", kwargs={"handle": other_namespace_object.handle}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Namespace.objects.filter(handle=other_namespace_object.handle).exists()
        )

    def test_namespace_activation_view_unauthorized(self):
        # Create another user's namespace
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        other_namespace = Namespace.objects.create(
            user=other_user,
            handle="other-namespace",
        )

        url = reverse(
            "django_namespaces:activate", kwargs={"handle": other_namespace.handle}
        )

        # Test both GET and POST methods
        for method in [self.client.get, self.client.post]:
            response = method(url)
            self.assertEqual(
                response.status_code,
                404,
                f"Expected 404 for {method.__name__}, got {response.status_code}",
            )

    def test_htmx_list_view(self):
        response = self.client.get(
            reverse("django_namespaces:list"), HTTP_HX_REQUEST="true"
        )
        self.assertTemplateUsed(
            response, "django_namespaces/snippets/namespace_list.html"
        )

    def test_success_messages(self):
        from django.contrib.messages import get_messages

        # Test create success message
        new_handle = "message-test"
        response = self.client.post(
            reverse("django_namespaces:create"), {"handle": new_handle}, follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"{new_handle} was created successfully.")
        # Clear message storage
        storage = get_messages(response.wsgi_request)
        list(storage)  # Consume messages

        # Test update success message
        updated_handle = "message-test-updated"
        response = self.client.post(
            reverse("django_namespaces:detail-update", kwargs={"handle": new_handle}),
            {
                "handle": updated_handle,
                "title": "Updated Title",
                "description": "Updated description",
            },
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), f"{updated_handle} was updated.")

        # Clear message storage
        storage = get_messages(response.wsgi_request)
        list(storage)  # Consume messages

        # Test delete success message
        response = self.client.post(
            reverse(
                "django_namespaces:delete", kwargs={"handle": "message-test-updated"}
            ),
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), "Namespace was deleted successfully.")

    def test_clear_namespaces_view(self):
        # Test GET request (should redirect)
        response = self.client.get(reverse("django_namespaces:clear"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("django_namespaces:list"))

        # Test POST request
        response = self.client.post(reverse("django_namespaces:clear"), follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "All namespaces deactivated.")

    def test_namespace_activation_with_htmx(self):
        url = reverse(
            "django_namespaces:activate", kwargs={"handle": self.namespace.handle}
        )

        # Test HTMX request
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")

        # Test regular request with success message
        response = self.client.get(url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"{self.namespace.handle} activated.")
        self.assertEqual(
            response.redirect_chain[0][0],
            settings.DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL,
        )

    def test_namespace_detail_context(self):
        url = reverse(
            "django_namespaces:detail-update",
            kwargs={"handle": self.namespace.handle},
        )
        response = self.client.get(url)
        self.assertIn("activated", response.context)
        self.assertIsInstance(response.context["activated"], bool)
