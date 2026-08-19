# from fastapi import APIRouter, Request

# from app.schemas.chat import (
#     ChatRequest,
#     ChatResponse,
# )
# from app.services.chat_service import ChatService


# router = APIRouter(
#     prefix="/api/v1/chat",
#     tags=["chat"],
# )


# @router.post(
#     "",
#     response_model=ChatResponse,
# )
# async def chat(
#     request: Request,
#     body: ChatRequest,
# ):

#     service = ChatService(
#         request.app.state.chatbot
#     )

#     return await service.chat(
#         message=body.message,
#         thread_id=body.thread_id,
#     )


import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatRequest,
    ConversationResponse,
    ThreadListResponse,
)
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)


def sse_event(data: dict) -> str:
    """
    Convert a dictionary into an SSE event.
    """

    return f"data: {json.dumps(data)}\n\n"


@router.post("/stream")
async def stream_chat(
    body: ChatRequest,
    request: Request,
):

    service = ChatService(
        chatbot=request.app.state.chatbot,
        checkpointer=(
            request.app.state
            .checkpointer_manager
            .checkpointer
        ),
    )

    async def event_generator():

        async for event in service.stream_chat(
            message=body.message,
            thread_id=body.thread_id,
        ):
            yield sse_event(event)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get(
    "/threads",
    response_model=ThreadListResponse,
)
async def list_threads(request: Request):

    service = ChatService(
        chatbot=request.app.state.chatbot,
        checkpointer=(
            request.app.state
            .checkpointer_manager
            .checkpointer
        ),
    )

    threads = await service.list_threads()

    return {
        "threads": threads,
    }


@router.get(
    "/{thread_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    thread_id: str,
    request: Request,
):

    service = ChatService(
        chatbot=request.app.state.chatbot,
        checkpointer=(
            request.app.state
            .checkpointer_manager
            .checkpointer
        ),
    )

    return await service.get_conversation(
        thread_id
    )