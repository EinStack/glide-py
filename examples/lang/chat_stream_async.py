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
question = "How are you?"


async def chat_stream() -> None:
    glide_client = AsyncGlideClient(base_url="http://127.0.0.1:9099/v1/")

    print(f"💬Question: {question}")
    print("💬Answer: ", end="")

    last_msg: Optional[ChatStreamMessage] = None
    chat_req = ChatStreamRequest(message=ChatMessage(role="user", content=question))

    started_at = time.perf_counter()
    first_chunk_recv_at: Optional[float] = None

    try:
        async with glide_client.lang.stream_client(router_id) as client:
            async for message in client.chat_stream(chat_req):
                if not first_chunk_recv_at:
                    first_chunk_recv_at = time.perf_counter()

                last_msg = message

                if err := message.error:
                    print(f"💥ERR: {err.message} (code: {err.err_code})")
                    print("🧹 Restarting the stream")
                    continue

                if content_chunk := message.content_chunk:
                    print(content_chunk, end="", flush=True)
                    continue

                raise RuntimeError(f"Unknown message type: {last_msg}")

            if last_msg and last_msg.chunk and last_msg.finish_reason:
                # LLM gen context
                provider_name = last_msg.chunk.provider_name
                model_name = last_msg.chunk.model_name
                finish_reason = last_msg.finish_reason

                print(
                    f"\n\n✅ Generation is done "
                    f"(provider: {provider_name}, model: {model_name}, reason: {finish_reason.value})"
                )

                print(
                    f"👀Glide Context (router_id: {last_msg.router_id}, model_id: {last_msg.chunk.model_id})"
                )

            first_chunk_duration_ms: float = 0

            if first_chunk_recv_at:
                first_chunk_duration_ms = (first_chunk_recv_at - started_at) * 1_000
                print(f"\n⏱️First Response Chunk: {first_chunk_duration_ms:.2f}ms")

            chat_duration_ms = (time.perf_counter() - started_at) * 1_000

            print(
                f"⏱️Chat Duration: {chat_duration_ms:.2f}ms "
                f"({(chat_duration_ms - first_chunk_duration_ms):.2f}ms after the first chunk)"
            )
    except Exception as e:
        print(f"💥Stream interrupted by ERR: {e}")


if __name__ == "__main__":
    asyncio.run(chat_stream())
