from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

import django_namespaces
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


class NamespaceCreateView(LoginRequiredMixin, SuccessMessageMixin,CreateView):
    model = Namespace
    form_class = NamespaceCreateForm
    success_message = "%(namespace)s was created successfully."

    def get_template_names(self):
        request = self.request
        if hasattr(request, "htmx"):
            if request.htmx:
                return ["django_namespaces/snippets/namespace_create.html"]
        return ["django_namespaces/namespace_create.html"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NamespaceDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = Namespace
    form_class = NamespaceUpdateForm
    success_message = "%(namespace)s was updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object.namespace == self.request.namespace, self.object.namespace, self.request.namespace)
        print(type(self.object.namespace), type(self.request.namespace))
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


class NamespaceDeleteConfirmationView(LoginRequiredMixin, DeleteView):
    model = Namespace
    success_message = "%(namespace)s was deleted successfully."

    def get_success_url(self):
        return utils.reverse("django_namespaces:list")

    def get_template_names(self):
        request = self.request
        if hasattr(request, "htmx"):
            if request.htmx:
                return ["django_namespaces/snippets/namespace_delete.html"]
        return ["django_namespaces/namespace_delete.html"]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)



def namespace_activation_view(request, slug=None):
    try:
        obj = Namespace.objects.get(user=request.user, slug=slug)
    except Namespace.DoesNotExist:
        return HttpResponse("Invalid namespace")
    except Namespace.MultipleObjectsReturned:
        return HttpResponse("Invalid namespace")
    django_namespaces.activate(request, namespace=obj.namespace, namespace_id=str(obj.id))
    if hasattr(request, "htmx"):
        if request.htmx:
            return HttpResponse("OK")
    return HttpResponseRedirect(settings.DJANGO_NAMESPACE_ACTIVATION_REDIRECT_URL)


def clear_namespaces_view(request):
    namespace_list_view = utils.reverse("django_namespaces:list")
    if request.method == "POST":
        django_namespaces.clear(request)
        return HttpResponseRedirect(namespace_list_view)
    return HttpResponseRedirect(namespace_list_view)
    
