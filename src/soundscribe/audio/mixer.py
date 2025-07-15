"""Audio mixing system using FFmpeg."""

import asyncio
import logging
import subprocess
from typing import List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class AudioMixer:
    """Handles mixing multiple audio streams into a single file."""
    
    def __init__(self):
        self.ffmpeg_path = "ffmpeg"
    
    async def mix_audio_files(
        self, 
        audio_files: List[Tuple[str, float]], 
        output_path: str, 
        total_duration: float
    ):
        """
        Mix multiple audio files into a single output file.
        
        Args:
            audio_files: List of (file_path, start_offset) tuples
            output_path: Path for the output mixed file
            total_duration: Total duration of the recording session
        """
        if not audio_files:
            raise ValueError("No audio files to mix")
        
        if len(audio_files) == 1:
            # Single file - just convert to MP3
            await self._convert_single_file(audio_files[0][0], output_path)
        else:
            # Multiple files - mix them
            await self._mix_multiple_files(audio_files, output_path, total_duration)
    
    async def _convert_single_file(self, input_path: str, output_path: str):
        """Convert a single audio file to MP3."""
        cmd = [
            self.ffmpeg_path,
            "-y",  # Overwrite output file
            "-i", input_path,
            "-acodec", "libmp3lame",
            "-ab", "128k",
            output_path
        ]
        
        await self._run_ffmpeg(cmd)
        logger.info(f"Converted single file: {input_path} -> {output_path}")
    
    async def _mix_multiple_files(
        self, 
        audio_files: List[Tuple[str, float]], 
        output_path: str, 
        total_duration: float
    ):
        """Mix multiple audio files with proper timing."""
        # Build FFmpeg command for mixing
        cmd = [self.ffmpeg_path, "-y"]
        
        # Add input files
        for file_path, _ in audio_files:
            cmd.extend(["-i", file_path])
        
        # Create filter graph for mixing
        # For now, we'll use a simple amix filter
        num_inputs = len(audio_files)
        filter_complex = f"amix=inputs={num_inputs}:duration=longest:dropout_transition=2"
        
        cmd.extend([
            "-filter_complex", filter_complex,
            "-acodec", "libmp3lame",
            "-ab", "128k",
            output_path
        ])
        
        await self._run_ffmpeg(cmd)
        logger.info(f"Mixed {num_inputs} files into: {output_path}")
    
    async def _run_ffmpeg(self, cmd: List[str]):
        """Run FFmpeg command asynchronously."""
        try:
            logger.debug(f"Running FFmpeg: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown FFmpeg error"
                raise RuntimeError(f"FFmpeg failed with code {process.returncode}: {error_msg}")
                
            logger.debug("FFmpeg completed successfully")
            
        except Exception as e:
            logger.error(f"FFmpeg execution failed: {e}")
            raise