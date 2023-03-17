from django.urls import path

from . import views

app_name="django_namespaces"
urlpatterns = [
    path("", views.NamespaceListView.as_view(), name="list"),
    path("create/", views.NamespaceCreateView.as_view(), name="create"),
    path("<slug:handle>/", views.NamespaceDetailUpdateView.as_view(), name="detail-update"),
    path("<slug:handle>/activate/", views.namespace_activation_view, name="activate"),
    path("<slug:handle>/confirm-delete/", views.NamespaceDeleteConfirmationView.as_view(), name="delete"),
]