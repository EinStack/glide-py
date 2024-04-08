# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import asyncio
import time

from glide import AsyncGlideClient
from glide.lang import ChatRequest, ChatMessage

router_id: str = "default"  # defined in Glide config (see glide.config.yaml)


async def chat() -> None:
    glide_client = AsyncGlideClient(base_url="http://127.0.0.1:9099/v1/")

    question = "What's the capital of Germany?"
    started_at = time.perf_counter()

    response = await glide_client.lang.chat(
        router_id=router_id,
        request=ChatRequest(
            message=ChatMessage(
                content=question,
                role="user",
            ),
        ),
    )

    duration_ms = (time.perf_counter() - started_at) * 1000

    print(f"💬Question: {question}")
    print(f"💬Answer: {response.model_response.message.content}")
    print(f"⏱️Response Time: {duration_ms:.2f}ms")


if __name__ == "__main__":
    asyncio.run(chat())
