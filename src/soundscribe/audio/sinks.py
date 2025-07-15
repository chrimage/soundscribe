"""Custom audio sinks for multi-stream recording."""

import io
import logging
from typing import Dict, Optional
import discord

logger = logging.getLogger(__name__)


class MultiStreamSink(discord.sinks.Sink):
    """Custom sink that captures audio from multiple users separately."""
    
    def __init__(self):
        super().__init__()
        self.encoding = "wav"
        self.audio_data: Dict[int, AudioData] = {}
    
    def wants_opus(self) -> bool:
        """We want decoded audio for processing."""
        return False
    
    def write(self, data, user):
        """Write audio data from a specific user."""
        if user not in self.audio_data:
            self.audio_data[user] = AudioData()
        
        self.audio_data[user].write(data)
    
    def cleanup(self):
        """Clean up resources."""
        for audio in self.audio_data.values():
            audio.cleanup()
        self.audio_data.clear()


class AudioData:
    """Stores audio data for a single user."""
    
    def __init__(self):
        self.file = io.BytesIO()
        self._closed = False
    
    def write(self, data: bytes):
        """Write audio data."""
        if not self._closed:
            self.file.write(data)
    
    def close(self):
        """Close the audio data."""
        self._closed = True
    
    def cleanup(self):
        """Clean up resources."""
        if hasattr(self.file, 'close'):
            self.file.close()