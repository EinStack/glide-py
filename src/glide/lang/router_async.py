# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
from typing import List

import httpx
import pydantic

from glide.exceptions import GlideUnavailable, GlideClientError, GlideClientMismatch
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
    async def chat(
        self,
        router_id: str,
        request: schemas.ChatRequest,
    ) -> schemas.ChatResponse:
        """
        Send a chat request to a specified language router
        """
        try:
            resp = await self._http_client.post(
                f"/language/{router_id}/chat",
                json=request.dict(by_alias=True),
            )
        except httpx.NetworkError as e:
            raise GlideUnavailable() from e

        if not resp.is_success:
            raise GlideClientError(
                f"Failed to send a chat request: {resp.text} (status_code: {resp.status_code})"
            )

        try:
            raw_response = resp.json()

            return schemas.ChatResponse(**raw_response)
        except pydantic.ValidationError as err:
            raise GlideClientMismatch(
                "Failed to validate Glide API response. Please make sure Glide API and client versions are compatible"
            ) from err

    async def chat_stream(self, router_id: str): ...
