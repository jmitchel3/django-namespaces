from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

import django_namespaces
from django_namespaces import resolvers
from django_namespaces import utils
from django_namespaces.conf import settings
from django_namespaces.import_utils import import_module_from_str

Namespace = import_module_from_str(settings.DJANGO_NAMESPACE_MODEL)
NamespaceCreateForm = import_module_from_str(settings.DJANGO_NAMESPACE_CREATE_FORM)
NamespaceUpdateForm = import_module_from_str(settings.DJANGO_NAMESPACE_UPDATE_FORM)


class NamespaceListView(LoginRequiredMixin, ListView):
    model = Namespace

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_template_names(self):
        request = self.request
        if hasattr(request, "htmx"):
            if request.htmx:
                return ["django_namespaces/snippets/namespace_list.html"]
        return ["django_namespaces/namespace_list.html"]


class NamespaceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Namespace
    form_class = NamespaceCreateForm
    success_message = "%(handle)s was created successfully."

    def get_template_names(self):
        request = self.request
        if hasattr(request, "htmx"):
            if request.htmx:
                return ["django_namespaces/snippets/namespace_create.html"]
        return ["django_namespaces/namespace_create.html"]

    def get_success_url(self):
        utils.set_user_cached_namespaces(self.request.user)
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NamespaceDetailUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Namespace
    form_class = NamespaceUpdateForm
    success_message = "%(handle)s was updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activated"] = self.object.namespace == self.request.namespace
        return context

    def get_template_names(self):
        request = self.request
        if hasattr(request, "htmx"):
            if request.htmx:
                return ["django_namespaces/snippets/namespace_update.html"]
        return ["django_namespaces/namespace_update.html"]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), handle=self.kwargs.get("handle"))


class NamespaceDeleteConfirmationView(
    LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Namespace
    success_message = "Namespace was deleted successfully."

    def get_success_url(self):
        utils.set_user_cached_namespaces(self.request.user)
        return resolvers.reverse("django_namespaces:list")

    def get_template_names(self):
        request = self.request
        if hasattr(request, "htmx"):
            if request.htmx:
                return ["django_namespaces/snippets/namespace_delete.html"]
        return ["django_namespaces/namespace_delete.html"]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), handle=self.kwargs.get("handle"))


def namespace_activation_view(request, handle=None):
    # Get the namespace, returning 404 if not found or not owned by user
    namespace = get_object_or_404(Namespace, user=request.user, handle=handle)

    django_namespaces.activate(
        request, namespace=namespace.namespace, namespace_id=str(namespace.id)
    )

    if hasattr(request, "htmx"):
        if request.htmx:
            return HttpResponse("OK")

    messages.success(request, f"{handle} activated.")
    return HttpResponseRedirect(settings.DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL)


def clear_namespaces_view(request):
    namespace_list_view = resolvers.reverse("django_namespaces:list")
    if request.method == "POST":
        django_namespaces.clear(request)
        messages.success(request, "All namespaces deactivated.")
        return HttpResponseRedirect(namespace_list_view)
    return HttpResponseRedirect(namespace_list_view)
