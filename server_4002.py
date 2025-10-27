"""
Logging server on port 4002 that receives and displays logs.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Logging Server")


class LogMessage(BaseModel):
    """Model for log messages."""
    message: str


@app.post("/log")
async def receive_log(log: LogMessage):
    """
    Receive and display log messages.
    Prints to terminal with timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_output = f"[{timestamp}] {log.message}"
    print(log_output)
    
    return {"status": "logged", "timestamp": timestamp}


@app.get("/")
async def root():
    """Root endpoint with usage information."""
    return {
        "message": "Logging Server",
        "usage": "POST /log - Receive log messages"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4002)
