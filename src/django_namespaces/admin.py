from __future__ import annotations

import swapper
from django.contrib import admin

Namespace = swapper.load_model("django_namespaces", "Namespace")


class NamespaceAdmin(admin.ModelAdmin):
    list_display = ["handle", "title", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["handle", "title", "user__username"]

    class Meta:
        model = Namespace


# Only register if the model hasn't been swapped
if not swapper.is_swapped("django_namespaces", "Namespace"):
    admin.site.register(Namespace, NamespaceAdmin)
