# from contextlib import asynccontextmanager

# from fastapi import FastAPI

# from app.core.config import get_settings
# from app.db.checkpointer import CheckpointerManager
# from app.graph.builder import build_graph
# from app.graph.tools import load_all_tools


# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     settings = get_settings()

#     # -------------------------
#     # Database
#     # -------------------------

#     checkpointer_manager = CheckpointerManager(
#         settings.database_url
#     )

#     checkpointer = await checkpointer_manager.start()

#     # -------------------------
#     # MCP + other tools
#     # -------------------------

#     tools = await load_all_tools()

#     # -------------------------
#     # LangGraph
#     # -------------------------

#     chatbot = build_graph(
#         tools=tools,
#         checkpointer=checkpointer,
#     )

#     # Store application resources
#     app.state.chatbot = chatbot
#     app.state.checkpointer_manager = checkpointer_manager
#     app.state.tools = tools

#     print(
#         f"Application started with {len(tools)} tools"
#     )

#     try:
#         yield

#     finally:

#         await checkpointer_manager.close()

#         print("Application shutdown complete")



from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.checkpointer import CheckpointerManager
from app.graph.builder import build_graph
from app.graph.tools import load_all_tools


@asynccontextmanager
async def lifespan(app: FastAPI):

    settings = get_settings()

    # -------------------------
    # Database
    # -------------------------

    checkpointer_manager = CheckpointerManager(
        settings.database_url
    )

    checkpointer = await checkpointer_manager.start()

    # -------------------------
    # Tools + MCP
    # -------------------------

    tools = await load_all_tools()

    print(
        f"Loaded {len(tools)} tools"
    )

    # -------------------------
    # LangGraph
    # -------------------------

    chatbot = build_graph(
        tools=tools,
        checkpointer=checkpointer,
    )

    app.state.chatbot = chatbot
    app.state.tools = tools
    app.state.checkpointer_manager = (
        checkpointer_manager
    )

    print("Backend started")

    try:
        yield

    finally:

        await checkpointer_manager.close()

        print("Backend stopped")