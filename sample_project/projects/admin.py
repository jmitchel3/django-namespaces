from __future__ import annotations

from django.contrib import admin

from .models import Namespace

# from django_namespaces.models import Namespace as DjangoNamespace


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    list_display = ["handle"]
    search_fields = ["handle"]
    # list_filter = ()


# admin.site.unregister(DjangoNamespace)
