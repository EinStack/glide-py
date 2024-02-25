# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import asyncio

from glide import AsyncGlideClient
from glide.lang import ChatRequest, ChatMessage

router_id: str = "default"  # defined in Glide config (see glide.config.yaml)


async def chat() -> None:
    glide_client = AsyncGlideClient(base_url="http://127.0.0.1:9099/v1/")

    response = await glide_client.lang.chat(
        router_id=router_id,
        request=ChatRequest(
            message=ChatMessage(
                content="What's the capital of Germany?",
                role="user",
            ),
        ),
    )

    print("Model Response: ", response.model_response.message.content)


if __name__ == "__main__":
    asyncio.run(chat())
