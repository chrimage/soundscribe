#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

import sys
import traceback

def test_imports():
    """Test importing all major components."""
    print("Testing SoundScribe imports...")
    
    try:
        print("✓ Importing FastAPI...")
        import fastapi
        
        print("✓ Importing uvicorn...")
        import uvicorn
        
        print("✓ Importing pathlib...")
        from pathlib import Path
        
        print("✓ Importing asyncio...")
        import asyncio
        
        print("✓ Importing logging...")
        import logging
        
        # Test individual modules without Discord for now
        print("✓ Testing audio mixer...")
        from src.soundscribe.audio.mixer import AudioMixer
        mixer = AudioMixer()
        
        print("✓ Testing download server...")
        from src.soundscribe.server import DownloadServer
        server = DownloadServer()
        
        print("\n🎉 All imports successful!")
        print("Note: Discord-related imports skipped due to Python 3.13 compatibility issue.")
        print("Recommend using Python 3.12 for full functionality.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)