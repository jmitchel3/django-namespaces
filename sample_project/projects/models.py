from __future__ import annotations

import uuid

from django.db import models

from django_namespaces import validators
from django_namespaces.conf import settings as django_namespace_settings

# from django.conf import settings

# Create your models here.


class Namespace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    handle = models.SlugField(
        help_text="Namespaces must be unique across this website.",
        max_length=django_namespace_settings.DJANGO_NAMESPACES_MAX_HANDLE_LENGTH,
        validators=[validators.valid_project_id],
        unique=True,
    )
