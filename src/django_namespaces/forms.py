from __future__ import annotations

import swapper
from django import forms

from django_namespaces.conf import settings

Namespace = swapper.load_model("django_namespaces", "Namespace")


def get_fields():
    from django_namespaces.models import Namespace as _Namespace

    if Namespace == _Namespace:
        return ["title", "handle", "description"]
    else:
        return settings.DJANGO_NAMESPACE_FIELDS


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
        fields = get_fields()
