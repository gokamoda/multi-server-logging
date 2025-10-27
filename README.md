# multi-server-logging

A multi-server application that demonstrates inter-server communication and logging.

## Overview

This project consists of two components:

1. **Server 4001 (Power of 2 Calculator)**: An interactive terminal application that prompts users to enter integers and calculates their power of 2 (number squared). Before returning the result, it sends a non-blocking log request to the logging server.

2. **Server 4002 (Logging Server)**: A FastAPI logging server that receives log messages and displays them in the terminal with timestamps.

## Requirements

- Python 3.7+
- HTTPX (for server 4001)
- FastAPI and Uvicorn (for server 4002)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gokamoda/multi-server-logging.git
cd multi-server-logging
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Servers

You need to run both servers in separate terminal windows.

### Terminal 1: Start the Logging Server (Port 4002)

```bash
python server_4002.py
```

The logging server will start on `http://localhost:4002` and display received logs in the terminal.

### Terminal 2: Start the Interactive Power Calculator

```bash
python server_4001.py
```

The calculator will start in interactive mode, prompting you to enter integers.

## Usage

### Interactive Mode (Terminal 2)

Once server_4001.py is running, you'll see:

```
Power of 2 Calculator (Interactive Mode)
==================================================
Enter integers to calculate their power of 2 (number^2)
Type 'quit' or 'exit' to stop
==================================================

Enter a number: 5
Result: 5^2 = 25

Enter a number: 10
Result: 10^2 = 100

Enter a number: quit
Goodbye!
```

### In Terminal 1 (Logging Server):

You should see log entries with timestamps:
```
[2025-10-27 14:22:30] Calculated power of 2 for number: 5, result: 25
[2025-10-27 14:22:35] Calculated power of 2 for number: 10, result: 100
```

## Features

- **Interactive Terminal UI**: Direct input/output in the terminal for quick calculations
- **Non-blocking Logging**: Uses fire-and-forget pattern to avoid blocking the calculator
- **Timestamped Logs**: All calculations are logged with timestamps to the logging server
- **Error Handling**: Gracefully handles invalid inputs and network errors

## API Documentation

### Server 4002 (Logging)

- **GET /**: Root endpoint with usage information
- **POST /log**: Receive and display log messages
  - Body: JSON with `message` field
  - Returns: JSON with status and timestamp

### Interactive API Documentation

FastAPI provides automatic interactive API documentation for the logging server:

- Server 4002: http://localhost:4002/docs
