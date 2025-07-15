#!/usr/bin/env python3
"""
Standalone script to run the SoundScribe bot.
This can be used for development and testing.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("soundscribe.log")
    ]
)

# Import and run the bot
from src.soundscribe import main

if __name__ == "__main__":
    main()