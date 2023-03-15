import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import smart_str

from django_namespaces import resolvers, validators
from django_namespaces.conf import settings as django_namespace_settings


class Namespace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(help_text='Namespaces must be unique across this website.', 
        max_length=django_namespace_settings.DJANGO_NAMESPACE_MAX_SLUG_LENGTH, 
        validators=[validators.valid_project_id], 
        unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['slug', '-updated_at', '-created_at']

    def get_absolute_url(self):
        """
        defaults to django.urls.reverse
        Review django_namespaces.resolvers for more
        """
        return resolvers.reverse('django_namespaces:detail-update', kwargs={'slug': self.namespace})

    def get_activation_url(self):
        """
        defaults to django.urls.reverse
        Review django_namespaces.resolvers for more
        """
        return resolvers.reverse('django_namespaces:activate', kwargs={'slug': self.namespace})

    def get_delete_url(self):
        """
        defaults to django.urls.reverse
        Review django_namespaces.resolvers for more
        """
        return resolvers.reverse('django_namespaces:delete', kwargs={'slug': self.namespace})
    
    def __str__(self):
        return self.namespace

    @property
    def namespace(self):
        return smart_str(self.slug)


class AnonymousNamespace(object):
    slug = None
