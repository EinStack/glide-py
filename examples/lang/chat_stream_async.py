# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import asyncio

from glide import AsyncGlideClient
from glide.lang.schemas import ChatStreamError

router_id: str = "default"  # defined in Glide config (see glide.config.yaml)


async def chat_stream() -> None:
    glide_client = AsyncGlideClient(base_url="http://127.0.0.1:9099/v1/")

    question = "What's the most complex physics theory of all time?"

    print(f"💬Question: {question}")
    print("💬Answer:", end=" ")

    async with glide_client.lang.stream_client(router_id) as stream_client:
        async for resp_chunk in await stream_client.chat_stream():
            if isinstance(resp_chunk, ChatStreamError):
                print(f"💥err: {resp_chunk.message} (code: {resp_chunk.err_code})")
                continue

            print(resp_chunk.model_response.message.content, end=" ")

    # started_at = time.perf_counter()
    # duration_ms = (time.perf_counter() - started_at) * 1000

    # print(f"💬Answer: {response.model_response.message.content}")
    # print(f"⏱️Response Time: {duration_ms:.2f}ms")


if __name__ == "__main__":
    asyncio.run(chat_stream())
