"""
Interactive server on port 4001 that computes square (n^2) for a given integer.
Logs requests to the logging server on port 4002.
"""
import asyncio
from remote_logger import RemoteLogger


LOGGING_SERVER_URL = "http://localhost:4002/log"
remote_logger = RemoteLogger(endpoint=LOGGING_SERVER_URL, server_name="InteractiveServer")




async def calculate_square(number: int) -> int:
    """Calculate n^2 for a given integer."""
    result = number ** 2
    remote_logger.log(f"Calculated square for {number}: {result}")
    return result


async def main():
    """Main interactive loop."""
    print("Square Calculator (Interactive Mode)")
    print("=" * 50)
    print("Enter integers to calculate n^2")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 50)

    while True:
        try:
            # 入力は別スレッドで実行し、イベントループを止めない
            user_input = await asyncio.to_thread(lambda: input("\nEnter a number: ").strip())
            if user_input.lower() in {"quit", "exit", "q"}:
                print("Goodbye!")
                break

            try:
                number = int(user_input)
                result = await calculate_square(number)
                print(f"Result: {number}^2 = {result}")
            except ValueError:
                print("Invalid input! Please enter an integer.")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())