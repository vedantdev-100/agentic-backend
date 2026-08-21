from langchain_core.messages import ToolMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from pydantic import SecretStr

from app.core.config import get_settings
from app.graph.state import ChatState


settings = get_settings()


def create_llm(tools):
    llm = ChatGroq(
        model=settings.model_name,
        api_key=SecretStr(settings.groq_api_key),
        temperature=0,
    )

    return llm.bind_tools(tools)


def create_chat_node(llm_with_tools):
    async def chat_node(state: ChatState):
        response = await llm_with_tools.ainvoke(
            state["messages"]
        )

        return {
            "messages": [response]
        }

    return chat_node


def sanitize_tool_messages(state: ChatState):
    """
    Groq can reject empty/malformed tool messages.

    Normalize all ToolMessage content into a non-empty string.
    """

    fixed = []
    changed = False

    for message in state["messages"]:

        if isinstance(message, ToolMessage):

            content = message.content

            if not content:
                message = message.model_copy(
                    update={
                        "content": "No result returned."
                    }
                )

                changed = True

            elif isinstance(content, list):

                text = " ".join(
                    block.get("text", "")
                    if isinstance(block, dict)
                    else str(block)
                    for block in content
                )

                if not text.strip():
                    text = "No result returned."

                message = message.model_copy(
                    update={
                        "content": text
                    }
                )

                changed = True

        fixed.append(message)

    if changed:
        return {
            "messages": fixed
        }

    return {}


def create_tool_node(tools):
    return ToolNode(tools)