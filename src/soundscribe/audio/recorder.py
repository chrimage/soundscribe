"""Audio recording system with multi-stream capture and processing."""

import os
import time
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import discord

from .mixer import AudioMixer
from .sinks import MultiStreamSink

logger = logging.getLogger(__name__)


class AudioRecorder:
    """Manages audio recording sessions with multi-stream capture."""
    
    def __init__(self, recordings_dir: str = "recordings"):
        self.recordings_dir = Path(recordings_dir)
        self.recordings_dir.mkdir(exist_ok=True)
        
        self.is_recording = False
        self.current_session: Optional[RecordingSession] = None
        self.mixer = AudioMixer()
    
    async def start_recording(self, voice_client: discord.VoiceClient, guild_id: int):
        """Start recording in the given voice channel."""
        if self.is_recording:
            raise RuntimeError("Already recording")
        
        self.current_session = RecordingSession(guild_id, self.recordings_dir)
        self.is_recording = True
        
        # Create custom sink for multi-stream recording
        sink = MultiStreamSink()
        
        # Start recording
        voice_client.start_recording(
            sink,
            self._recording_finished_callback,
            self.current_session
        )
        
        logger.info(f"Started recording session {self.current_session.session_id}")
    
    async def stop_recording(self) -> Optional[str]:
        """Stop the current recording and process audio."""
        if not self.is_recording or not self.current_session:
            return None
        
        self.is_recording = False
        
        # The voice client's stop_recording() will trigger the callback
        # We'll wait for the session to complete processing
        while not self.current_session.is_complete:
            await asyncio.sleep(0.1)
        
        return self.current_session.final_audio_path
    
    async def handle_voice_state_update(self, member, before, after):
        """Handle user joining/leaving voice channel during recording."""
        if not self.is_recording or not self.current_session:
            return
        
        await self.current_session.handle_voice_state_update(member, before, after)
    
    def get_latest_recording(self) -> Optional[str]:
        """Get the path to the most recent recording."""
        if not self.recordings_dir.exists():
            return None
        
        mp3_files = list(self.recordings_dir.glob("*.mp3"))
        if not mp3_files:
            return None
        
        # Sort by modification time, newest first
        latest = max(mp3_files, key=lambda f: f.stat().st_mtime)
        return str(latest)
    
    async def _recording_finished_callback(self, sink: MultiStreamSink, session: "RecordingSession"):
        """Called when recording stops."""
        try:
            await session.process_recording(sink, self.mixer)
        except Exception as e:
            logger.error(f"Failed to process recording: {e}")
        finally:
            if session == self.current_session:
                self.current_session = None


class RecordingSession:
    """Represents a single recording session."""
    
    def __init__(self, guild_id: int, recordings_dir: Path):
        self.guild_id = guild_id
        self.session_id = self._generate_session_id()
        self.recordings_dir = recordings_dir
        self.start_time = time.time()
        
        # Track users and their audio segments
        self.user_segments: Dict[int, List[Tuple[float, str]]] = {}
        self.is_complete = False
        self.final_audio_path: Optional[str] = None
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"recording_{self.guild_id}_{timestamp}"
    
    async def handle_voice_state_update(self, member, before, after):
        """Handle voice state changes during recording."""
        # Track when users join/leave for potential future features
        user_id = member.id
        current_time = time.time() - self.start_time
        
        if before.channel is None and after.channel is not None:
            # User joined
            logger.debug(f"User {member.display_name} joined at {current_time:.2f}s")
        elif before.channel is not None and after.channel is None:
            # User left
            logger.debug(f"User {member.display_name} left at {current_time:.2f}s")
    
    async def process_recording(self, sink: MultiStreamSink, mixer: AudioMixer):
        """Process the recorded audio into a final mixed file."""
        try:
            if not sink.audio_data:
                logger.warning("No audio data recorded")
                self.is_complete = True
                return
            
            # Save individual audio files temporarily
            temp_files = []
            session_duration = time.time() - self.start_time
            
            for user_id, audio in sink.audio_data.items():
                if audio.file:
                    temp_file = self.recordings_dir / f"{self.session_id}_user_{user_id}.wav"
                    
                    # Save the audio file
                    audio.file.seek(0)
                    with open(temp_file, 'wb') as f:
                        f.write(audio.file.read())
                    
                    temp_files.append((str(temp_file), 0.0))  # Start at 0.0 for now
                    logger.debug(f"Saved audio for user {user_id}: {temp_file}")
            
            if temp_files:
                # Mix all audio files
                final_path = self.recordings_dir / f"{self.session_id}.mp3"
                await mixer.mix_audio_files(temp_files, str(final_path), session_duration)
                
                # Clean up temporary files
                for temp_file, _ in temp_files:
                    try:
                        os.unlink(temp_file)
                    except FileNotFoundError:
                        pass
                
                self.final_audio_path = str(final_path)
                logger.info(f"Recording session complete: {self.final_audio_path}")
            
        except Exception as e:
            logger.error(f"Failed to process recording session: {e}")
        finally:
            self.is_complete = True