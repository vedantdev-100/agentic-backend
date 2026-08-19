import aiosqlite

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


class CheckpointerManager:

    def __init__(self, database: str):
        self.database = database
        self.connection = None
        self.checkpointer = None

    async def start(self):
        self.connection = await aiosqlite.connect(
            self.database
        )

        self.checkpointer = AsyncSqliteSaver(
            self.connection
        )

        return self.checkpointer

    async def close(self):
        if self.connection:
            await self.connection.close()