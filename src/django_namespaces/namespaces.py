import logging

logger = logging.getLogger(__name__)


def activate(request, namespace=None, namespace_id=None):
    """
    Activate a namespace
    """
    try:
        del request.session["namespace"]
    except KeyError:
        logger.warning("Namespace not found in session")
    except Exception as e:
        logger.error(f"Error clearing namespace: {e}")
    request.session["namespace"] = namespace
    if namespace_id is not None:
        request.session["namespace_id"] = str(namespace_id)
    return


def clear(request):
    """
    Clear the namespace from the request object and session
    """
    activate(request, namespace=None)
