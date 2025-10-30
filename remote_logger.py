from pydantic import BaseModel
import httpx
import asyncio

class LogMessage(BaseModel):
    """Model for log messages."""
    message: str
    server_name: str
    level: str = "info"
    args: list = []


class RemoteLogger:
    endpoint: str
    server_name: str 

    def __init__(self, endpoint: str, server_name: str):
        self.endpoint = endpoint
        self.server_name = server_name

    def log(self, message: str, level: str, args) -> None:
        """Send log message to the logging server."""
        if not self.endpoint:
            return  # ロギングサーバーのエンドポイントが設定されていない場合は何もしない

        async def _send():
            try:
                async with httpx.AsyncClient(timeout=2.0) as client:
                    await client.post(
                        self.endpoint,
                        json={
                            "message": message,
                            "server_name": self.server_name,
                            "level": level,
                            "args": args,
                        },
                    )
            except Exception as e:
                # ロギングに失敗しても何もしない（要求仕様）
                pass

        try:
            asyncio.get_running_loop().create_task(_send())
        except RuntimeError:
            # イベントループがない環境では黙って捨てる（要求仕様）
            pass

    def critical(self, message: str, *args) -> None:
        """Log a critical level message."""
        self.log(message, level="critical", args=args)

    def fatal(self, message: str, *args) -> None:
        """Log a fatal level message."""
        self.log(message, level="fatal", args=args)

    def error(self, message: str, *args) -> None:
        """Log an error level message."""
        self.log(message, level="error", args=args)

    def warning(self, message: str, *args) -> None:
        """Log a warning level message."""
        self.log(message, level="warning", args=args)

    def info(self, message: str, *args) -> None:
        """Log an info level message."""
        self.log(message, level="info", args=args)

    def debug(self, message: str, *args) -> None:
        """Log a debug level message."""
        self.log(message, level="debug", args=args)
