#!/usr/bin/env python3
"""
Alternative implementation using discord.py instead of py-cord for voice.
Sometimes different libraries handle voice connections better on servers.
"""

import os
import asyncio
import logging
from dotenv import load_dotenv

# Load environment
load_dotenv()

# This is a test to see if regular discord.py works better
print("Testing with regular discord.py...")
print("Note: This requires installing discord.py instead of py-cord")
print("To test: pip install discord.py[voice] (but don't do this yet)")

# For now, let's try a simpler approach with py-cord
import discord
from discord.ext import commands

class SimpleVoiceTest(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
    
    async def on_ready(self):
        print(f'Bot ready: {self.user}')
    
    @commands.command()
    async def test_voice(self, ctx):
        """Simple voice connection test."""
        if ctx.author.voice:
            try:
                # Try connecting with minimal configuration
                channel = ctx.author.voice.channel
                await ctx.send("Attempting simple voice connection...")
                
                # Connect without any recording - just test the connection
                vc = await channel.connect(timeout=10.0)
                await ctx.send("✅ Voice connection successful!")
                
                # Disconnect immediately
                await vc.disconnect()
                await ctx.send("✅ Disconnected successfully")
                
            except asyncio.TimeoutError:
                await ctx.send("❌ Connection timed out")
            except Exception as e:
                await ctx.send(f"❌ Error: {e}")
        else:
            await ctx.send("Join a voice channel first!")

if __name__ == "__main__":
    bot = SimpleVoiceTest()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if token:
        bot.run(token)
    else:
        print("No bot token found!")