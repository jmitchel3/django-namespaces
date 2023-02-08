import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import smart_str

from django_namespaces import validators
from django_namespaces.conf import settings as django_namespace_settings


class Namespace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(help_text='Namespaces must be unique across this Django project.', max_length=django_namespace_settings.DJANGO_NAMESPACE_MAX_SLUG_LENGTH, validators=[validators.valid_project_id], unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_str(self.slug)


class AnonymousNamespace(object):
    slug = None
