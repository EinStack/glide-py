# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
from typing import List

import httpx

from glide.lang import schemas


class AsyncLangRouters:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    async def get_routers(self) -> List[schemas.LangRouter]:
        """
        Get list of language routers configured in a Glide cluster
        """
        ...

    # TODO: expose timeout config here, too
    async def chat(self, router_id: str, request: schemas.ChatRequest) -> schemas.ChatResponse:
        """
        Send a chat request to a specified language router
        """
        resp = await self._http_client.post(
            f"/language/{router_id}/chat",
            data=request.dict(),
        )

        # TODO: think about useful error cases to handle here.

        return schemas.ChatResponse(**resp.json())

    async def chat_stream(self, router_id: str):
        ...
