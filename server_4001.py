"""
Interactive server on port 4001 that computes power of 2 for a given integer.
Logs requests to the logging server on port 4002.
"""
import httpx
import asyncio

LOGGING_SERVER_URL = "http://localhost:4002/log"


def send_log_fire_and_forget(log_message: str):
    """Send log to logging server without blocking (fire and forget)."""
    async def _send():
        try:
            async with httpx.AsyncClient() as client:
                await client.post(LOGGING_SERVER_URL, json={"message": log_message})
        except Exception:
            pass

    # Get the running event loop and create task
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(_send())
    except RuntimeError:
        # If no event loop is running, skip logging
        pass


async def calculate_power_of_2(number: int) -> int:
    """Calculate the power of 2 for a given integer."""
    result = number ** 2
    
    # Send log to logging server (fire and forget)
    log_message = f"Calculated power of 2 for number: {number}, result: {result}"
    send_log_fire_and_forget(log_message)
    
    return result


async def main():
    """Main interactive loop."""
    print("Power of 2 Calculator (Interactive Mode)")
    print("=" * 50)
    print("Enter integers to calculate their power of 2 (number^2)")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nEnter a number: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            try:
                number = int(user_input)
                result = await calculate_power_of_2(number)
                print(f"Result: {number}^2 = {result}")
                # Give the fire-and-forget task a moment to complete
                await asyncio.sleep(0.1)
            except ValueError:
                print("Invalid input! Please enter an integer.")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
