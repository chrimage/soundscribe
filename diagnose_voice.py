#!/usr/bin/env python3
"""
Diagnose voice connection issues and check dependencies.
"""

import sys
import subprocess
import importlib.util

def check_voice_dependencies():
    """Check if voice dependencies are properly installed."""
    print("🔍 Checking voice dependencies...")
    
    # Check PyNaCl (required for voice)
    try:
        import nacl
        print("✓ PyNaCl installed")
    except ImportError:
        print("❌ PyNaCl not found - required for voice encryption")
        return False
    
    # Check if opus is available
    try:
        import discord
        print("✓ Discord.py/Pycord installed")
        
        # Check if opus encoder is available
        if hasattr(discord, 'opus'):
            if discord.opus.is_loaded():
                print("✓ Opus encoder loaded")
            else:
                print("⚠️  Opus encoder not loaded")
        else:
            print("⚠️  Opus module not found")
            
    except ImportError:
        print("❌ Discord library not installed")
        return False
    
    # Check FFmpeg for voice support
    try:
        result = subprocess.run(
            ["ffmpeg", "-codecs"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if "libopus" in result.stdout:
            print("✓ FFmpeg with opus support found")
        else:
            print("⚠️  FFmpeg found but opus codec might be missing")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg not found or not working")
        return False
    
    return True

def check_system_requirements():
    """Check system-level requirements for voice."""
    print("\n🖥️  Checking system requirements...")
    
    # Check if running on a server without audio devices
    try:
        import os
        if os.getenv("DISPLAY") is None:
            print("⚠️  No DISPLAY environment variable (headless server)")
            print("   This is normal for server deployments")
        else:
            print("✓ Display environment detected")
    except:
        pass
    
    # Check if we can create UDP sockets (required for voice)
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.close()
        print("✓ UDP socket creation works")
    except Exception as e:
        print(f"❌ UDP socket creation failed: {e}")
        return False
    
    return True

def suggest_fixes():
    """Suggest potential fixes for voice connection issues."""
    print("\n🔧 Potential fixes for voice connection issues:")
    print()
    print("1. **Install voice dependencies:**")
    print("   uv add 'py-cord[voice]' --upgrade")
    print()
    print("2. **Check bot permissions:**")
    print("   - Connect permission in voice channel")
    print("   - Speak permission in voice channel")
    print("   - Use Voice Activity permission")
    print()
    print("3. **Server/Network issues:**")
    print("   - Check if UDP ports are blocked by firewall")
    print("   - Discord voice uses UDP ports 50000-65535")
    print("   - Ensure server can reach Discord voice endpoints")
    print()
    print("4. **Try different voice region:**")
    print("   - Discord server voice region might be having issues")
    print("   - Try changing server region in Discord settings")
    print()
    print("5. **Check Discord status:**")
    print("   - Visit https://discordstatus.com for service issues")

def main():
    """Run voice connection diagnostics."""
    print("🎤 SoundScribe Voice Connection Diagnostics\n")
    
    deps_ok = check_voice_dependencies()
    sys_ok = check_system_requirements()
    
    if deps_ok and sys_ok:
        print("\n✅ All basic checks passed!")
        print("Voice connection issues might be network or Discord-related.")
    else:
        print("\n❌ Some checks failed. See suggestions below.")
    
    suggest_fixes()

if __name__ == "__main__":
    main()