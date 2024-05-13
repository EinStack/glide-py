# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import asyncio
import time
from typing import Optional

from glide import AsyncGlideClient
from glide.lang.schemas import (
    ChatStreamRequest,
    ChatMessage,
    ChatStreamMessage,
)

router_id: str = "default"  # defined in Glide config (see glide.config.yaml)
question = "What is the most complicated theory discovered by humanity?"


async def chat_stream() -> None:
    glide_client = AsyncGlideClient(base_url="http://127.0.0.1:9099/v1/")

    print(f"💬Question: {question}")
    print("💬Answer: ", end="")

    last_msg: Optional[ChatStreamMessage] = None
    chat_req = ChatStreamRequest(message=ChatMessage(role="user", content=question))

    started_at = time.perf_counter()
    first_chunk_recv_at: Optional[float] = None

    async with glide_client.lang.stream_client(router_id) as client:
        try:
            async for message in client.chat_stream(chat_req):
                if not first_chunk_recv_at:
                    first_chunk_recv_at = time.perf_counter()

                last_msg = message

                if message.chunk:
                    print(message.content_chunk, end="", flush=True)
                    continue

                if err := message.error:
                    print(f"💥ERR ({err.name}): {err.message}")
                    print("🧹 Restarting the stream")
                    continue

                print(f"😮Unknown message type: {message}")
        except Exception as e:
            print(f"💥Stream interrupted by ERR: {e}")

        if last_msg and last_msg.chunk and last_msg.finish_reason:
            # LLM gen context
            provider_name = last_msg.chunk.provider_id
            model_name = last_msg.chunk.model_name
            finish_reason = last_msg.finish_reason

            print(
                f"\n\n✅ Generation is done "
                f"(provider: {provider_name}, model: {model_name}, reason: {finish_reason.value})"
            )

            print(
                f"👀Glide Context (router_id: {last_msg.router_id}, model_id: {last_msg.chunk.model_id})"
            )

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
