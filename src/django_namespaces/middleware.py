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
        namespace_obj = NamespaceDetails(request)  # type: ignore [attr-defined]     
        if namespace_obj.has_namespace:
            request.namespace = namespace_obj
        else:
            request.namespace = AnonymousNamespace()
        return self.get_response(request)

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        namespace_obj = NamespaceDetails(request)  # type: ignore [attr-defined]     
        if namespace_obj.has_namespace:
            request.namespace = namespace_obj
        else:
            request.namespace = AnonymousNamespace()
        result = self.get_response(request)
        assert not isinstance(result, HttpResponseBase)  # type narrow
        return await result


class AnonymousNamespace(object):
    value = None
    
class NamespaceDetails:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self._namespace = self.request.session.get("namespace") or ""
        self._namespace_id = str(self.request.session.get("namespace_id")) or None

    def __repr__(self) -> Optional[str]:
        return f"<Namespace {self._namespace}>"

    def __str__(self) -> str:
        return self._namespace
    
    @cached_property
    def value(self) -> str:
        return str(self._namespace)
    
    @cached_property
    def id(self) -> str:
        return self._namespace_id

    @cached_property
    def has_namespace(self) -> bool:
        return self._namespace != ""