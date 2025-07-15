#!/usr/bin/env python3
"""
Setup verification script for SoundScribe.
Checks all prerequisites and provides setup guidance.
"""

import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and 12 <= version.minor <= 12:
        print(f"✓ Python {version.major}.{version.minor} is supported")
        return True
    elif version.major == 3 and version.minor >= 13:
        print(f"⚠️  Python {version.major}.{version.minor} detected")
        print("   Discord libraries don't support Python 3.13+ yet")
        print("   Please use Python 3.12 for full functionality")
        return False
    else:
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Please use Python 3.12")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\n🎵 Checking FFmpeg...")
    
    if shutil.which("ffmpeg"):
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✓ {version_line}")
                return True
        except subprocess.TimeoutExpired:
            pass
    
    print("❌ FFmpeg not found")
    print("   Install FFmpeg:")
    print("   - Ubuntu/Debian: sudo apt install ffmpeg")
    print("   - macOS: brew install ffmpeg")
    print("   - Windows: Download from https://ffmpeg.org/")
    return False

def check_environment():
    """Check environment configuration."""
    print("\n⚙️  Checking environment...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file found")
        
        with open(env_file) as f:
            content = f.read()
            if "DISCORD_BOT_TOKEN=" in content and not "your_discord_bot_token_here" in content:
                print("✓ Discord bot token appears to be configured")
                return True
            else:
                print("⚠️  Discord bot token not configured in .env")
                return False
    else:
        print("⚠️  .env file not found")
        print("   Copy .env.example to .env and configure your bot token")
        return False

def check_dependencies():
    """Check if dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    try:
        import fastapi
        print("✓ FastAPI installed")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import uvicorn
        print("✓ Uvicorn installed")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    # Don't test Discord import in Python 3.13
    if sys.version_info >= (3, 13):
        print("⚠️  Discord library not tested (Python 3.13+)")
    else:
        try:
            import discord
            print("✓ Discord (Pycord) installed")
        except ImportError:
            print("❌ Discord (Pycord) not installed")
            return False
    
    return True

def check_directories():
    """Check required directories."""
    print("\n📁 Checking directories...")
    
    recordings_dir = Path("recordings")
    if not recordings_dir.exists():
        recordings_dir.mkdir()
        print("✓ Created recordings directory")
    else:
        print("✓ Recordings directory exists")
    
    return True

def main():
    """Run all setup checks."""
    print("🔧 SoundScribe Setup Verification\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Directories", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("📋 Setup Summary:")
    
    all_passed = True
    for name, passed in results:
        status = "✓" if passed else "❌"
        print(f"   {status} {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All checks passed! SoundScribe is ready to run.")
        print("   Start the bot with: python run_bot.py")
    else:
        print("\n⚠️  Some checks failed. Please resolve the issues above.")
        
        if sys.version_info >= (3, 13):
            print("\n💡 Quick fix for Python 3.13:")
            print("   Install Python 3.12 using pyenv or your package manager")
            print("   Then recreate the virtual environment with Python 3.12")

if __name__ == "__main__":
    main()