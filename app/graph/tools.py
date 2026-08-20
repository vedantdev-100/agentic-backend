# import requests

# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_core.tools import BaseTool, tool
# from langchain_mcp_adapters.client import MultiServerMCPClient

# from app.core.config import get_settings


# settings = get_settings()


# search_tool = DuckDuckGoSearchRun(region="us-en")


# @tool
# def get_stock_price(symbol: str) -> dict:
#     """
#     Fetch the latest stock price for a stock symbol.
#     Example: AAPL, TSLA.
#     """

#     url = (
#         "https://www.alphavantage.co/query"
#         f"?function=GLOBAL_QUOTE"
#         f"&symbol={symbol}"
#         f"&apikey={settings.alpha_vantage_api_key}"
#     )

#     response = requests.get(url, timeout=15)
#     response.raise_for_status()

#     return response.json()


# def create_mcp_client() -> MultiServerMCPClient:
#     return MultiServerMCPClient(
#         {
#             "arith": {
#                 "transport": "stdio",
#                 "command": settings.arith_python,
#                 "args": [
#                     settings.arith_main,
#                 ],
#             },
#             "expense": {
#                 "transport": "streamable_http",
#                 "url": settings.expense_mcp_url,
#                 "headers": {
#                     "Authorization": (
#                         f"Bearer {settings.fastmcp_api_key}"
#                     ),
#                 },
#             },
#         }
#     )


# async def load_mcp_tools() -> list[BaseTool]:
#     client = create_mcp_client()

#     try:
#         return await client.get_tools()
#     except Exception as exc:
#         print(f"Failed to load MCP tools: {exc}")
#         return []


# async def load_all_tools() -> list[BaseTool]:
#     mcp_tools = await load_mcp_tools()

#     return [
#         search_tool,
#         get_stock_price,
#         *mcp_tools,
#     ]


import traceback
import requests

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import get_settings


settings = get_settings()


# ============================================================
# Regular tools
# ============================================================

search_tool = DuckDuckGoSearchRun(
    region="us-en"
)


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the latest stock price for a stock symbol.
    Example: AAPL, TSLA.
    """

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={settings.alpha_vantage_api_key}"
    )

    response = requests.get(
        url,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# MCP client
# ============================================================

def create_mcp_client() -> MultiServerMCPClient:

    return MultiServerMCPClient(
        {
            # -------------------------
            # Local arithmetic MCP
            # -------------------------
            # "arith": {
            #     "transport": "stdio",
            #     "command": settings.arith_python,
            #     "args": [
            #         settings.arith_main,
            #     ],
            # },

            # -------------------------
            # Remote expense MCP
            # -------------------------
            "expense": {
                "transport": "streamable_http",
                "url": settings.expense_mcp_url,
                "headers": {
                    "Authorization": (
                        f"Bearer "
                        f"{settings.fastmcp_api_key}"
                    ),
                },
            },
        }
    )


# ============================================================
# Load MCP tools
# ============================================================

async def load_mcp_tools() -> list[BaseTool]:

    client = create_mcp_client()

    try:

        print("Loading MCP tools...")

        tools = await client.get_tools()

        print(
            f"Successfully loaded "
            f"{len(tools)} MCP tools"
        )

        for tool_item in tools:
            print(
                f"  - {tool_item.name}"
            )

        return tools

    except Exception:

        print(
            "\n================ MCP ERROR ================\n"
        )

        traceback.print_exc()

        print(
            "\n============================================\n"
        )

        return []


# ============================================================
# Load all tools
# ============================================================

async def load_all_tools() -> list[BaseTool]:

    print("Loading application tools...")

    mcp_tools = await load_mcp_tools()

    tools = [
        search_tool,
        get_stock_price,
        *mcp_tools,
    ]

    print(
        f"Total tools loaded: {len(tools)}"
    )

    return tools