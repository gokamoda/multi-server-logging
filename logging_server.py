"""
Logging server on port 4002 that receives and displays logs.
"""

import logging
from logging import _nameToLevel
from datetime import datetime
from time import sleep

import uvicorn
from fastapi import FastAPI
from pytz import timezone
from rich.logging import RichHandler

from remote_logger import LogMessage

app = FastAPI(title="Logging Server")


def _custom_time(*args):
    return datetime.now(timezone("Asia/Tokyo")).timetuple()


def init_logger():
    """Initialize a custom logger that prints to terminal."""
    logger = logging.getLogger("LoggingServer")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(message)s"
    )

    formatter.converter = _custom_time

    # console handler
    ch = RichHandler(
        rich_tracebacks=False,
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True,
    )
    ch.setLevel(0)
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
    level_str = log.level.upper()
    level_int = _nameToLevel.get(level_str, logging.INFO)
    logger.log(level_int, f"[{log.server_name}]\n{log.message}\n", *log.args)
    return {"status": "logged"}


@app.get("/")
async def root():
    """Root endpoint with usage information."""
    return {"message": "Logging Server", "usage": "POST /log - Receive log messages"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4002, log_level="error")
