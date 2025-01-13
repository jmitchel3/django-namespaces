from __future__ import annotations

import logging

from django.http import HttpRequest

logger = logging.getLogger(__name__)


def activate(
    request: HttpRequest, namespace: str | None = None, namespace_id: str | None = None
) -> None:
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


def clear(request: HttpRequest) -> None:
    """
    Clear the namespace from the request object and session
    """
    activate(request, namespace=None)
