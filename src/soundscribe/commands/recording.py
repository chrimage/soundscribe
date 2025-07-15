"""Recording-related slash commands."""

import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


def setup_recording_commands(bot):
    """Set up recording commands on the bot."""
    
    @bot.slash_command(description="Join your voice channel and start recording")
    async def join(ctx: discord.ApplicationContext):
        """Join the user's voice channel and start recording."""
        # Check if user is in a voice channel
        if not ctx.author.voice:
            await ctx.respond("❌ You need to be in a voice channel first!", ephemeral=True)
            return
        
        # Check if already recording
        if bot.audio_recorder.is_recording:
            await ctx.respond("❌ Already recording in another channel!", ephemeral=True)
            return
        
        try:
            # Connect to voice channel
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
            bot.voice_connections[ctx.guild.id] = vc
            
            # Start recording
            await bot.audio_recorder.start_recording(vc, ctx.guild.id)
            
            await ctx.respond(f"🎙️ Started recording in {voice_channel.name}!", ephemeral=True)
            logger.info(f"Started recording in {voice_channel.name} (Guild: {ctx.guild.id})")
            
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            await ctx.respond(f"❌ Failed to start recording: {str(e)}", ephemeral=True)
    
    @bot.slash_command(description="Stop recording and process audio")
    async def stop(ctx: discord.ApplicationContext):
        """Stop the current recording and process audio."""
        if not bot.audio_recorder.is_recording:
            await ctx.respond("❌ Not currently recording!", ephemeral=True)
            return
        
        if ctx.guild.id not in bot.voice_connections:
            await ctx.respond("❌ Not recording in this server!", ephemeral=True)
            return
        
        try:
            await ctx.respond("⏹️ Stopping recording and processing audio...", ephemeral=True)
            
            # Stop recording and get the file path
            audio_file_path = await bot.audio_recorder.stop_recording()
            
            # Disconnect from voice
            vc = bot.voice_connections.get(ctx.guild.id)
            if vc and vc.is_connected():
                await vc.disconnect()
            del bot.voice_connections[ctx.guild.id]
            
            if audio_file_path:
                # Generate download link
                download_url = await bot.download_server.create_download_link(audio_file_path)
                
                embed = discord.Embed(
                    title="🎵 Recording Complete",
                    description="Your recording has been processed and is ready for download.",
                    color=discord.Color.green()
                )
                embed.add_field(name="Download", value=f"[Click here to download]({download_url})", inline=False)
                embed.add_field(name="Note", value="Download link expires in 1 hour", inline=False)
                
                await ctx.followup.send(embed=embed, ephemeral=True)
                logger.info(f"Recording completed: {audio_file_path}")
            else:
                await ctx.followup.send("❌ No audio was recorded!", ephemeral=True)
                
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            await ctx.followup.send(f"❌ Failed to stop recording: {str(e)}", ephemeral=True)
    
    @bot.slash_command(description="Get download link for the last recording")
    async def last_recording(ctx: discord.ApplicationContext):
        """Get a download link for the most recent recording."""
        try:
            latest_file = bot.audio_recorder.get_latest_recording()
            if not latest_file:
                await ctx.respond("❌ No recordings found!", ephemeral=True)
                return
            
            # Generate download link
            download_url = await bot.download_server.create_download_link(latest_file)
            
            embed = discord.Embed(
                title="🎵 Latest Recording",
                description="Download link for your most recent recording.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Download", value=f"[Click here to download]({download_url})", inline=False)
            embed.add_field(name="Note", value="Download link expires in 1 hour", inline=False)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Failed to get last recording: {e}")
            await ctx.respond(f"❌ Failed to get recording: {str(e)}", ephemeral=True)