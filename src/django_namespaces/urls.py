from django.urls import path

from . import views

app_name="django_namespaces"
urlpatterns = [
    path("", views.NamespaceListView.as_view(), name="list"),
    path("create/", views.NamespaceCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.NamespaceDetailUpdateView.as_view(), name="detail-update"),
    path("<slug:slug>/activate/", views.namespace_activation_view, name="activate"),
    path("<slug:slug>/confirm-delete/", views.NamespaceDeleteConfirmationView.as_view(), name="delete"),
]