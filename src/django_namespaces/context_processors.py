from django_namespaces import utils


def user_namespaces(request):
    if request.user.is_authenticated:
        return {
            "user_namespaces": get_or_set_cached_user_namespaces(request.user)
        }
    return {}
