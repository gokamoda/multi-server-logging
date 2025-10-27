# multi-server-logging

A multi-server application that demonstrates inter-server communication and logging with an interactive terminal interface.

## Overview

This project consists of three main components:

1. **main_server.py (Port 4001)**: An interactive terminal application (Square Calculator) that prompts users to enter integers and calculates their square (n²). Uses non-blocking fire-and-forget pattern to send logs to the logging server.

2. **logging_server.py (Port 4002)**: A FastAPI server that receives log messages from remote servers and displays them in the terminal with colorful formatting and timestamps in Asia/Tokyo timezone.

3. **remote_logger.py**: A reusable logging utility class that provides non-blocking, fire-and-forget logging to the remote logging server.

## Requirements

- Python 3.12+
- FastAPI (for logging server)
- Uvicorn (for logging server)
- HTTPX (for remote logging)
- Rich (for colorful terminal output)
- pytz (for timezone support)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gokamoda/multi-server-logging.git
cd multi-server-logging
```

2. Install dependencies using pip:
```bash
pip install fastapi uvicorn httpx rich pytz
```

Or using uv (recommended):
```bash
uv pip install -e .
```

## Running the Application

You need to run both servers in separate terminal windows.

### Terminal 1: Start the Logging Server (Port 4002)

```bash
python logging_server.py
```

The logging server will start on `http://localhost:4002` and display received logs in the terminal with colorful formatting.

### Terminal 2: Start the Interactive Square Calculator (Port 4001)

```bash
python main_server.py
```

The calculator will start in interactive mode, prompting you to enter integers.

## Usage

### Interactive Mode (Terminal 2 - main_server.py)

Once the main server is running, you'll see:

```
Square Calculator (Interactive Mode)
==================================================
Enter integers to calculate n^2
Type 'quit' or 'exit' to stop
==================================================

Enter a number: 5
Result: 5^2 = 25

Enter a number: 10
Result: 10^2 = 100

Enter a number: quit
Goodbye!
```

### Logging Output (Terminal 1 - logging_server.py)

You should see log entries with timestamps in colorful format:
```
2025/10/27 14:22:30 [InteractiveServer] Calculated square for 5: 25

2025/10/27 14:22:35 [InteractiveServer] Calculated square for 10: 100
```

## Architecture

### RemoteLogger Class

The `RemoteLogger` class in `remote_logger.py` provides a clean interface for sending logs to the remote server:

```python
from remote_logger import RemoteLogger

# Create a logger instance
logger = RemoteLogger(
    endpoint="http://localhost:4002/log",
    server_name="MyService"
)

# Send logs (non-blocking)
logger.log("This is a log message")
```

**Key Features:**
- **Non-blocking**: Uses `asyncio.create_task()` for fire-and-forget logging
- **Error Handling**: Silently fails if the logging server is unavailable
- **Server Identification**: Each log includes the server name for easy tracking

### Logging Server API

The logging server exposes a FastAPI REST API:

- **GET /**: Root endpoint with usage information
- **POST /log**: Receive and display log messages
  - Request Body: JSON with `message` (str) and `server_name` (str) fields
  - Response: JSON with `status` field

### Interactive API Documentation

FastAPI provides automatic interactive API documentation for the logging server:

- Swagger UI: http://localhost:4002/docs
- ReDoc: http://localhost:4002/redoc

## Features

- **Interactive Terminal UI**: Direct input/output in the terminal for quick calculations
- **Non-blocking Logging**: Uses fire-and-forget pattern with asyncio to avoid blocking the main application
- **Colorful Logs**: Rich library provides beautiful, colorful terminal output for the logging server
- **Timezone Support**: Logs are displayed with timestamps in Asia/Tokyo timezone
- **Server Identification**: Each log message includes the originating server name
- **Error Handling**: Gracefully handles invalid inputs, network errors, and unavailable logging servers
- **Async Input**: Uses `asyncio.to_thread()` to prevent blocking the event loop during user input

## Code Structure

```
multi-server-logging/
├── main_server.py          # Interactive square calculator (port 4001)
├── logging_server.py       # FastAPI logging server (port 4002)
├── remote_logger.py        # Reusable remote logging utility
├── pyproject.toml          # Project dependencies and configuration
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check .
```

### Type Checking

```bash
mypy .
```

## License

This project is open source and available for educational purposes.
