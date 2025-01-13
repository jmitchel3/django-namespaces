from django.urls import path

from .views import (
    NamespaceCreateView,
    NamespaceDeleteConfirmationView,
    NamespaceDetailUpdateView,
    NamespaceListView,
    namespace_activation_view,
)

app_name = "django_namespaces"
urlpatterns = [
    path("", NamespaceListView.as_view(), name="list"),
    path("create/", NamespaceCreateView.as_view(), name="create"),
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
