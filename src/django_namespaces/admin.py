from django.contrib import admin

from django_namespaces.conf import settings
from django_namespaces.import_utils import import_module_from_str

Namespace = import_module_from_str(settings.DJANGO_NAMESPACE_MODEL)


class NamespaceAdmin(admin.ModelAdmin):
    list_display = ["handle", "title", "user", "modified"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["handle", "title", "user__username"]

    class Meta:
        model = Namespace


admin.site.register(Namespace)
