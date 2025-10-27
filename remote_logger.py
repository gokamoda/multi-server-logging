import asyncio

import httpx
from pydantic import BaseModel


class LogMessage(BaseModel):
    """Model for log messages."""

    message: str
    server_name: str


class RemoteLogger:
    endpoint: str
    server_name: str

    def __init__(self, endpoint: str, server_name: str):
        self.endpoint = endpoint
        self.server_name = server_name

    def log(self, message: str) -> None:
        """Send log message to the logging server."""

        async def _send():
            try:
                async with httpx.AsyncClient(timeout=2.0) as client:
                    await client.post(
                        self.endpoint,
                        json={"message": message, "server_name": self.server_name},
                    )
            except Exception as e:
                print(f"Logging failed: {e}")

        try:
            asyncio.get_running_loop().create_task(_send())
        except RuntimeError:
            # イベントループがない環境では黙って捨てる（要求仕様）
            pass
