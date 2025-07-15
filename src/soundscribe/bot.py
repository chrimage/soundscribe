"""Main Discord bot class and core functionality."""

import os
import asyncio
import logging
from typing import Dict, Optional
import discord
from discord.ext import commands

from .audio.recorder import AudioRecorder
from .server import DownloadServer


logger = logging.getLogger(__name__)


class SoundScribeBot(discord.Bot):
    """Main SoundScribe Discord bot class."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.message_content = True
        
        super().__init__(
            intents=intents,
            debug_guilds=None  # Set to a list of guild IDs for testing
        )
        
        # Core components
        self.audio_recorder = AudioRecorder()
        self.download_server: Optional[DownloadServer] = None
        
        # Connection tracking
        self.voice_connections: Dict[int, discord.VoiceClient] = {}
        
        # Load commands
        self._load_commands()
    
    def _load_commands(self):
        """Load slash commands."""
        from .commands.recording import setup_recording_commands
        setup_recording_commands(self)
    
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info(f"SoundScribe logged in as {self.user}")
        
        # Start download server
        if not self.download_server:
            self.download_server = DownloadServer()
            await self.download_server.start()
            logger.info("Download server started")
    
    async def on_voice_state_update(self, member, before, after):
        """Handle voice state changes for recording purposes."""
        if self.audio_recorder.is_recording:
            await self.audio_recorder.handle_voice_state_update(member, before, after)
    
    def run(self, token: Optional[str] = None):
        """Run the bot with token from environment if not provided."""
        if token is None:
            token = os.getenv("DISCORD_BOT_TOKEN")
            if not token:
                raise ValueError("DISCORD_BOT_TOKEN environment variable not set")
        
        super().run(token)
    
    async def close(self):
        """Clean shutdown of the bot."""
        logger.info("Shutting down SoundScribe...")
        
        # Stop any active recordings
        if self.audio_recorder.is_recording:
            await self.audio_recorder.stop_recording()
        
        # Stop download server
        if self.download_server:
            await self.download_server.stop()
        
        # Disconnect from voice channels
        for vc in self.voice_connections.values():
            if vc.is_connected():
                await vc.disconnect()
        
        await super().close()