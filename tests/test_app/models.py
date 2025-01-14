from __future__ import annotations

from django.db import models


class ValidNamespaceModel(models.Model):
    handle = models.SlugField(unique=True)

    class Meta:
        app_label = "test_app"


class InvalidNamespaceModel(models.Model):
    # Missing handle field
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "test_app"


class WrongFieldTypeNamespaceModel(models.Model):
    handle = models.CharField(max_length=100)  # Should be SlugField

    class Meta:
        app_label = "test_app"


class NonUniqueHandleNamespaceModel(models.Model):
    handle = models.SlugField(unique=False)  # Should be unique

    class Meta:
        app_label = "test_app"
