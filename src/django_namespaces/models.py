from __future__ import annotations

import uuid

import swapper
from django.conf import settings
from django.db import models
from django.utils.encoding import smart_str

from django_namespaces import resolvers
from django_namespaces import validators
from django_namespaces.conf import settings as django_namespace_settings


class AbstractNamespace(models.Model):
    """
    Abstract base class for all namespace models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    handle = models.SlugField(
        help_text="Namespaces must be unique across this website.",
        max_length=django_namespace_settings.DJANGO_NAMESPACE_MAX_HANDLE_LENGTH,
        validators=[validators.valid_project_id],
        unique=True,
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(
        default=True, help_text="Default namespace for this user (only one possible)"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.default:
            NamespaceModel = swapper.load_model("django_namespaces", "Namespace")
            qs = NamespaceModel.objects.filter(user=self.user, default=True).exclude(
                id=self.id
            )
            qs.update(default=False)

    class Meta:
        abstract = True
        ordering = ["handle", "-updated_at", "-created_at"]

    def get_absolute_url(self):
        """
        defaults to django.urls.reverse
        Review django_namespaces.resolvers for more
        """
        return resolvers.reverse(
            "django_namespaces:detail-update", kwargs={"handle": self.handle}
        )

    def get_activation_url(self):
        """
        defaults to django.urls.reverse
        Review django_namespaces.resolvers for more
        """
        return resolvers.reverse(
            "django_namespaces:activate", kwargs={"handle": self.handle}
        )

    def get_delete_url(self):
        """
        defaults to django.urls.reverse
        Review django_namespaces.resolvers for more
        """
        return resolvers.reverse(
            "django_namespaces:delete", kwargs={"handle": self.handle}
        )

    def __str__(self):
        return self.namespace

    @property
    def namespace(self):
        return smart_str(self.handle)


class Namespace(AbstractNamespace):
    """
    Namespace model.
    """

    class Meta(AbstractNamespace.Meta):
        abstract = False
        swappable = swapper.swappable_setting("django_namespaces", "Namespace")


class AnonymousNamespace:
    """
    Anonymous namespace.
    """

    handle = None
