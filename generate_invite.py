#!/usr/bin/env python3
"""
Generate a Discord bot invite link with the required permissions.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_invite_link():
    """Generate the bot invite link with required permissions."""
    
    # Get bot token to extract application ID
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not found in environment")
        print("   Make sure you have a .env file with your bot token")
        return
    
    # Extract application ID from token (first part before first dot)
    try:
        app_id = token.split('.')[0]
        # Decode base64 to get the actual application ID
        import base64
        app_id = base64.b64decode(app_id + '==').decode('utf-8')
    except:
        print("❌ Invalid bot token format")
        return
    
    # Required permissions for SoundScribe:
    # 2048 = Use Slash Commands
    # 3145728 = Connect + Speak (voice)
    # 2048 = Send Messages
    # Total: 3149824
    permissions = 3149824
    
    # Generate invite URL
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions={permissions}&scope=bot%20applications.commands"
    
    print("🔗 SoundScribe Bot Invite Link:")
    print(f"   {invite_url}")
    print()
    print("📋 Required Permissions:")
    print("   ✓ Send Messages")
    print("   ✓ Use Slash Commands") 
    print("   ✓ Connect (Voice)")
    print("   ✓ Speak (Voice)")
    print()
    print("💡 Instructions:")
    print("   1. Click the link above")
    print("   2. Select your Discord server")
    print("   3. Authorize the bot with the required permissions")
    print("   4. The bot will appear in your server")
    print("   5. Use /join in a voice channel to start recording")

if __name__ == "__main__":
    generate_invite_link()