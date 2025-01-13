from django import forms

from django_namespaces.conf import settings
from django_namespaces.import_utils import import_module_from_str

Namespace = import_module_from_str(settings.DJANGO_NAMESPACE_MODEL)


class NamespaceCreateForm(forms.ModelForm):
    handle = forms.SlugField(
        label="Namespace",
        help_text="Namespaces must be unique and can be changed later.",
    )

    class Meta:
        model = Namespace
        fields = ["handle"]


class NamespaceUpdateForm(forms.ModelForm):
    handle = forms.SlugField(
        label="Namespace",
        help_text="Namespaces must be unique and can be changed later.",
    )

    class Meta:
        model = Namespace
        fields = ["title", "handle", "description"]
