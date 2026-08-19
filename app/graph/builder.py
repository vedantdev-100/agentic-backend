from langgraph.graph import (
    END,
    START,
    StateGraph,
)
from langgraph.prebuilt import tools_condition

from app.graph.state import ChatState
from app.graph.nodes import (
    create_chat_node,
    create_llm,
    create_tool_node,
    sanitize_tool_messages,
)


def build_graph(tools, checkpointer):

    llm_with_tools = create_llm(tools)

    chat_node = create_chat_node(
        llm_with_tools
    )

    tool_node = create_tool_node(tools)

    graph = StateGraph(ChatState)

    graph.add_node(
        "chat_node",
        chat_node,
    )

    graph.add_node(
        "tools",
        tool_node,
    )

    graph.add_node(
        "sanitize",
        sanitize_tool_messages,
    )

    graph.add_edge(
        START,
        "chat_node",
    )

    graph.add_conditional_edges(
        "chat_node",
        tools_condition,
    )

    graph.add_edge(
        "tools",
        "sanitize",
    )

    graph.add_edge(
        "sanitize",
        "chat_node",
    )

    return graph.compile(
        checkpointer=checkpointer
    )