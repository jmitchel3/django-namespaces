from __future__ import annotations

from django.urls import path

from .views import clear_namespaces_view
from .views import namespace_activation_view
from .views import NamespaceCreateView
from .views import NamespaceDeleteConfirmationView
from .views import NamespaceDetailUpdateView
from .views import NamespaceListView

app_name = "django_namespaces"
urlpatterns = [
    path("", NamespaceListView.as_view(), name="list"),
    path("create/", NamespaceCreateView.as_view(), name="create"),
    path("clear/", clear_namespaces_view, name="clear"),
    path(
        "<slug:handle>/",
        NamespaceDetailUpdateView.as_view(),
        name="detail-update",
    ),
    path("<slug:handle>/activate/", namespace_activation_view, name="activate"),
    path(
        "<slug:handle>/confirm-delete/",
        NamespaceDeleteConfirmationView.as_view(),
        name="delete",
    ),
]
