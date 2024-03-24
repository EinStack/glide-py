# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import httpx

from glide.lang.router_async import AsyncLangRouters


class AsyncGlideClient:
    """
    Asynchronous Glide client
    """

    def __init__(
        self,
        base_url: str,
        # TODO: expose more configs like timeouts, limits, ssl
    ) -> None:
        """
        :param base_url: str The base URL of Glide API (by default, local API is under http://127.0.0.1:9099/v1/)
        """
        self._base_url = base_url
        self._client = httpx.AsyncClient(base_url=self._base_url)

        self._lang_routers = AsyncLangRouters(
            base_url=self._base_url,
            http_client=self._client,
        )

    @property
    def lang(self) -> AsyncLangRouters:
        """
        Access Glide's Language API
        """
        return self._lang_routers
