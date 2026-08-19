# from langchain_core.messages import HumanMessage


# class ChatService:

#     def __init__(self, chatbot):
#         self.chatbot = chatbot

#     async def chat(
#         self,
#         message: str,
#         thread_id: str,
#     ):

#         config = {
#             "configurable": {
#                 "thread_id": thread_id
#             }
#         }

#         result = await self.chatbot.ainvoke(
#             {
#                 "messages": [
#                     HumanMessage(content=message)
#                 ]
#             },
#             config=config,
#         )

#         messages = result["messages"]

#         last_message = messages[-1]

#         return {
#             "thread_id": thread_id,
#             "message": last_message.content,
#         }


from collections.abc import AsyncGenerator

from langchain_core.messages import HumanMessage


class ChatService:

    def __init__(self, chatbot, checkpointer):
        self.chatbot = chatbot
        self.checkpointer = checkpointer

    async def stream_chat(
        self,
        message: str,
        thread_id: str,
    ) -> AsyncGenerator[dict, None]:

        config = {
            "configurable": {
                "thread_id": thread_id,
            },
            "metadata": {
                "thread_id": thread_id,
            },
            "run_name": "chat_turn",
        }

        try:
            async for event in self.chatbot.astream_events(
                {
                    "messages": [
                        HumanMessage(content=message)
                    ]
                },
                config=config,
                version="v2",
            ):

                event_name = event.get("event")
                data = event.get("data", {})

                # -----------------------------
                # LLM streaming token
                # -----------------------------

                if event_name == "on_chat_model_stream":

                    chunk = data.get("chunk")

                    if chunk is None:
                        continue

                    content = getattr(
                        chunk,
                        "content",
                        "",
                    )

                    if isinstance(content, str) and content:
                        yield {
                            "type": "token",
                            "content": content,
                        }

                    elif isinstance(content, list):

                        for block in content:

                            if not isinstance(block, dict):
                                continue

                            text = block.get("text")

                            if text:
                                yield {
                                    "type": "token",
                                    "content": text,
                                }

                # -----------------------------
                # Tool started
                # -----------------------------

                elif event_name == "on_tool_start":

                    tool_name = event.get(
                        "name",
                        "tool",
                    )

                    yield {
                        "type": "tool_start",
                        "tool": tool_name,
                    }

                # -----------------------------
                # Tool finished
                # -----------------------------

                elif event_name == "on_tool_end":

                    tool_name = event.get(
                        "name",
                        "tool",
                    )

                    yield {
                        "type": "tool_end",
                        "tool": tool_name,
                    }

            yield {
                "type": "done",
            }

        except Exception as exc:

            yield {
                "type": "error",
                "message": str(exc),
            }

    async def get_conversation(
        self,
        thread_id: str,
    ):

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        state = await self.chatbot.aget_state(
            config=config
        )

        messages = state.values.get(
            "messages",
            [],
        )

        result = []

        for message in messages:

            message_type = message.__class__.__name__

            if message_type == "HumanMessage":
                role = "user"

            elif message_type == "AIMessage":
                role = "assistant"

            else:
                # Don't show tool messages in chat history
                continue

            content = message.content

            if isinstance(content, str):
                text = content

            elif isinstance(content, list):

                parts = []

                for block in content:

                    if isinstance(block, dict):
                        text = block.get("text")

                        if text:
                            parts.append(text)

                text = "".join(parts)

            else:
                text = str(content)

            if text:
                result.append(
                    {
                        "role": role,
                        "content": text,
                    }
                )

        return {
            "thread_id": thread_id,
            "messages": result,
        }

    async def list_threads(self):

        threads = set()

        async for checkpoint in self.checkpointer.alist(None):

            thread_id = (
                checkpoint.config
                .get("configurable", {})
                .get("thread_id")
            )

            if thread_id:
                threads.add(thread_id)

        return list(threads)