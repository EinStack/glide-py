# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import asyncio
import time
from typing import Optional

from glide import AsyncGlideClient
from glide.lang.schemas import (
    ChatStreamError,
    StreamChatRequest,
    ChatMessage,
    StreamResponse,
    ChatStreamChunk,
)

router_id: str = "default"  # defined in Glide config (see glide.config.yaml)
question = "What is the capital of Greenland?"


async def chat_stream() -> None:
    glide_client = AsyncGlideClient(base_url="http://127.0.0.1:9099/v1/")

    print(f"💬Question: {question}")
    print("💬Answer: ", end="")

    last_chunk: Optional[StreamResponse] = None
    chat_req = StreamChatRequest(message=ChatMessage(role="user", content=question))

    started_at = time.perf_counter()
    first_chunk_recv_at: Optional[float] = None

    async with glide_client.lang.stream_client(router_id) as client:
        async for chunk in client.chat_stream(chat_req):
            if not first_chunk_recv_at:
                first_chunk_recv_at = time.perf_counter()

            if isinstance(chunk, ChatStreamError):
                print(f"💥err: {chunk.message} (code: {chunk.err_code})")
                continue

            print(chunk.model_response.message.content, end="")
            last_chunk = chunk

    if last_chunk:
        if isinstance(last_chunk, ChatStreamChunk):
            if reason := last_chunk.model_response.finish_reason:
                print(f"\n✅ Generation is done (reason: {reason.value})")

        if isinstance(last_chunk, ChatStreamError):
            print(f"\n💥 Generation ended up with error (reason: {last_chunk.message})")

    first_chunk_duration_ms: float = 0

    if first_chunk_recv_at:
        first_chunk_duration_ms = (first_chunk_recv_at - started_at) * 1_000
        print(f"\n⏱️First Response Chunk: {first_chunk_duration_ms:.2f}ms")

    chat_duration_ms = (time.perf_counter() - started_at) * 1_000

    print(
        f"⏱️Chat Duration: {chat_duration_ms:.2f}ms "
        f"({(chat_duration_ms - first_chunk_duration_ms):.2f}ms after the first chunk)"
    )


if __name__ == "__main__":
    asyncio.run(chat_stream())
