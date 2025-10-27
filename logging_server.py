"""
Logging server on port 4002 that receives and displays logs.
"""
from fastapi import FastAPI

from datetime import datetime
import uvicorn
from remote_logger import LogMessage
import logging
from pytz import timezone
from rich.logging import RichHandler

app = FastAPI(title="Logging Server")

def _custom_time(*args):
    return datetime.now(timezone("Asia/Tokyo")).timetuple()

def init_logger():
    """Initialize a custom logger that prints to terminal."""
    logger = logging.getLogger("LoggingServer")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "\n%(asctime)s %(message)s",
        datefmt='%Y/%m/%d %H:%M:%S'
    )

    formatter.converter = _custom_time

    # console handler
    ch = RichHandler(
        rich_tracebacks=False,
        show_time=False,
        show_level=False,
        show_path=False,
    )
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

logger = init_logger()

@app.post("/log")
async def receive_log(log: LogMessage):
    """
    Receive and display log messages.
    Prints to terminal with timestamp.
    """
    logger.info(f"[{log.server_name}] {log.message}")
    return {"status": "logged"}


@app.get("/")
async def root():
    """Root endpoint with usage information."""
    return {
        "message": "Logging Server",
        "usage": "POST /log - Receive log messages"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4002, log_level="error")
