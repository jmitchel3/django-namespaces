from django import forms

from django_namespaces.conf import settings
from django_namespaces.import_utils import import_module_from_str

Namespace = import_module_from_str(settings.DJANGO_NAMESPACE_MODEL)



class NamespaceCreateForm(forms.ModelForm):
    slug = forms.SlugField(label='Namespace', help_text="Namespaces must be unique and can be changed later.")
    class Meta:
        model = Namespace
        fields = ["slug"]


class NamespaceUpdateForm(forms.ModelForm):
    slug = forms.SlugField(label='Namespace', help_text="Namespaces must be unique and can be changed later.")
    class Meta:
        model = Namespace
        fields = ["title", "slug", "description"]