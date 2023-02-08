from __future__ import annotations

import asyncio
import json
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import unquote, urlsplit, urlunsplit

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.functional import cached_property


class NamespaceMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
    ) -> None:
        self.get_response = get_response

        if asyncio.iscoroutinefunction(self.get_response):
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            self._is_coroutine = (
                asyncio.coroutines._is_coroutine  # type: ignore [attr-defined]
            )
        else:
            self._is_coroutine = None

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self._is_coroutine:
            return self.__acall__(request)
        namespace = NamespaceDetails(request)  # type: ignore [attr-defined]     
        print(namespace == "", namespace is None, type(namespace), namespace.has_namespace)
        if namespace.has_namespace:
            request.namespace = namespace
            request.has_namespace = True
        else:
            request.namespace = AnonymousNamespace()
            request.has_namespace = False
        return self.get_response(request)

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        namespace = NamespaceDetails(request)
        
        if namespace != "":
            request.namespace = namespace
            request.has_namespace = True
        else:
            request.namespace = AnonymousNamespace()
            request.has_namespace = False  # type: ignore [attr-defined]
        result = self.get_response(request)
        assert not isinstance(result, HttpResponseBase)  # type narrow
        return await result


class AnonymousNamespace(object):
    slug = None

    
class NamespaceDetails:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.namespace = (self.request.session.get("namespace") or "").strip()

    def __str__(self) -> Optional[str]:
        return self.namespace
    
    @cached_property
    def has_namespace(self) -> bool:
        return self.namespace != ""