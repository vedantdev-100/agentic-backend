from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=10000,
    )
    thread_id: str


class ChatResponse(BaseModel):
    thread_id: str
    message: str


class ThreadListResponse(BaseModel):
    threads: list[str]


class ConversationResponse(BaseModel):
    thread_id: str
    messages: list[dict]