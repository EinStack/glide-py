# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import asyncio
import re
from types import TracebackType
from typing import List, Optional, Type, Any, AsyncGenerator
from urllib.parse import urlparse, urlunparse, urljoin

import httpx
import pydantic
import websockets

from websockets import WebSocketClientProtocol

from glide.exceptions import GlideUnavailable, GlideClientError, GlideClientMismatch
from glide.lang import schemas
from glide.lang.schemas import StreamChatRequest, StreamResponse
from glide.typing import RouterId


class AsyncStreamChatClient:
    """
    Async Streaming Chat Client that opens a websocket connection for
    bidirectional message exchange between Glide and user applications
    """

    def __init__(
        self,
        base_url: str,
        router_id: RouterId,
        handlers: Optional[Any] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        self._base_url = self._validate_base_url(base_url)
        self._router_id = router_id

        self._user_agent = user_agent

        self._handlers = handlers

        self.requests: asyncio.Queue[StreamChatRequest] = asyncio.Queue()
        self.response_chunks: asyncio.Queue[StreamResponse] = asyncio.Queue()

        self._sender_task: Optional[asyncio.Task] = None
        self._receiver_task: Optional[asyncio.Task] = None

        self._ws_client: Optional[WebSocketClientProtocol] = None

    def request_chat(self, chat_request: StreamChatRequest) -> None:
        self.requests.put_nowait(chat_request)

    async def chat_stream(self) -> AsyncGenerator[StreamResponse, None]:
        pass

    async def start(self) -> None:
        self._ws_client = await websockets.connect(
            uri=urljoin(self._base_url, f"/language/{self._router_id}/chatStream"),
            user_agent_header=self._user_agent,
        )

        self._sender_task = asyncio.create_task(self._sender())
        self._receiver_task = asyncio.create_task(self._receiver())

    async def _sender(self) -> None:
        while self._ws_client and self._ws_client.open:
            try:
                chat_request = await self.requests.get()

                await self._ws_client.send(chat_request.json())
            except asyncio.CancelledError:
                # TODO: log
                ...

    async def _receiver(self) -> None:
        while self._ws_client and self._ws_client.open:
            try:
                raw_response_chunk = await self._ws_client.recv()

                print(raw_response_chunk)
                # TODO: impl
            except asyncio.CancelledError:
                # TODO: log
                ...

    async def stop(self) -> None:
        if self._sender_task:
            self._sender_task.cancel()
            await self._sender_task

        if self._receiver_task:
            self._receiver_task.cancel()
            await self._receiver_task

        if self._ws_client:
            await self._ws_client.close()

    async def __aenter__(self) -> "AsyncStreamChatClient":
        await self.start()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.stop()

    @staticmethod
    def _validate_base_url(base_url: str) -> str:
        parsed_url = urlparse(base_url)

        if parsed_url.scheme not in ("ws", "wss"):
            raise ValueError(
                f'Schema for Glide Streaming Chat must be websocket (e.g. ws:// or wss://), "{base_url}" given'
            )

        if not re.search(r"/v\d+/?", parsed_url.path):
            raise ValueError(
                f'Base URL must contain version subpath (e.g. /v1/), "{base_url}" given'
            )

        return base_url


class AsyncLangRouters:
    """
    Interact with Glide's language router API
    """

    def __init__(
        self,
        base_url: str,
        http_client: httpx.AsyncClient,
        user_agent: Optional[str] = None,
    ) -> None:
        self._base_url = base_url
        self._http_client = http_client
        self._user_agent = user_agent

    async def get_routers(self) -> List[schemas.LangRouter]:
        """
        Get list of language routers configured in a Glide cluster
        """
        raise NotImplementedError("Will be implemented in the next releases")

    # TODO: expose timeout config here, too
    async def chat(
        self,
        router_id: RouterId,
        request: schemas.ChatRequest,
    ) -> schemas.ChatResponse:
        """
        Send a chat request to a specified language router
        """
        try:
            headers = {}

            if self._user_agent:
                headers["User-Agent"] = self._user_agent

            resp = await self._http_client.post(
                f"/language/{router_id}/chat",
                headers=headers,
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

    def stream_client(self, router_id: RouterId) -> AsyncStreamChatClient:
        """
        Create a new async streaming chat client
        """
        return AsyncStreamChatClient(
            base_url=self._convert_http_to_ws_url(self._base_url),
            router_id=router_id,
            user_agent=self._user_agent,
        )

    @staticmethod
    def _convert_http_to_ws_url(http_base_url: str) -> str:
        parsed_http_url = urlparse(http_base_url)

        if parsed_http_url.scheme == "https":
            ws_scheme = "wss"
        elif parsed_http_url.scheme == "http":
            ws_scheme = "ws"
        else:
            raise ValueError("URL must be HTTP or HTTPS")

        parsed_ws_url = parsed_http_url._replace(scheme=ws_scheme)

        return str(urlunparse(parsed_ws_url))
