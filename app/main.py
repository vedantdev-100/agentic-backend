from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.core.lifespan import lifespan


app = FastAPI(
    title="LangGraph MCP Chatbot",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(chat_router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }