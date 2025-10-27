"""
Server on port 4001 that computes power of 2 for a given integer.
Logs requests to the logging server on port 4002.
"""
from fastapi import FastAPI, HTTPException
import httpx
import uvicorn

app = FastAPI(title="Power of 2 Server")

LOGGING_SERVER_URL = "http://localhost:4002/log"


@app.get("/power/{number}")
async def get_power_of_2(number: int):
    """
    Calculate the power of 2 for a given integer.
    Logs the request to the logging server before returning the result.
    """
    try:
        result = number ** 2
        
        # Send log to logging server
        log_message = f"Calculated power of 2 for number: {number}, result: {result}"
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    LOGGING_SERVER_URL,
                    json={"message": log_message},
                    timeout=2.0
                )
        except Exception as log_error:
            # Don't fail the request if logging fails
            print(f"Failed to send log: {log_error}")
        
        return {"number": number, "power_of_2": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with usage information."""
    return {
        "message": "Power of 2 Server",
        "usage": "GET /power/{number} - Calculate number^2"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4001)
