"""SoundScribe Discord Bot - Audio recording and mixing for voice channels."""

import asyncio
import signal
import sys


def main() -> None:
    """Main entry point for the SoundScribe bot."""
    # Import here to avoid circular imports and handle Discord compatibility issues
    try:
        from .bot import SoundScribeBot
    except ImportError as e:
        if "audioop" in str(e):
            print("Error: Python 3.13 is not compatible with Discord libraries.")
            print("Please use Python 3.12 or lower to run SoundScribe.")
            sys.exit(1)
        else:
            raise
    
    bot = SoundScribeBot()
    
    def signal_handler(signum, frame):
        print("\nShutting down SoundScribe...")
        asyncio.create_task(bot.close())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
