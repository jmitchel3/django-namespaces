from django.utils.decorators import method_decorator
from django.views import View

from django_namespaces.decorators import namespace_required


class NamespaceRequiredMixin(View):
    @method_decorator(namespace_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)