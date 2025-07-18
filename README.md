# SoundScribe Discord Bot

A Discord bot designed to solve the problem of transient voice conversations by creating a persistent, accessible audio archive. SoundScribe provides a simple, reliable way for users to record multi-speaker conversations and download a single mixed audio file.

## Features

- **Multi-Speaker Recording**: Captures separate audio streams for each user in a voice channel
- **Automatic Mixing**: Combines individual streams into a single synchronized MP3 file
- **Secure Downloads**: Provides temporary, token-based download links
- **Simple Commands**: Easy-to-use slash commands for recording control

## Commands

- `/join` - Join your voice channel and start recording
- `/stop` - Stop recording and process the audio
- `/last_recording` - Get a download link for the most recent recording

## Prerequisites

- Python 3.12+
- FFmpeg (for audio processing)
- Discord Bot Token

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd soundscribe
   ```

2. **Install dependencies with uv:**
   ```bash
   uv sync
   ```

3. **Configure the bot:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Discord bot token:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   ```

4. **Create a Discord bot:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and bot
   - Copy the bot token to your `.env` file
   - Enable the following bot permissions:
     - Send Messages
     - Use Slash Commands
     - Connect (Voice)
     - Speak (Voice)
     - Use Voice Activity

5. **Generate bot invite link:**
   ```bash
   python generate_invite.py
   ```
   
6. **Invite the bot to your server:**
   - Use the generated link to add the bot to your Discord server

## Usage

### Getting the Bot Invite Link

Before running the bot, you need to invite it to your Discord server:

```bash
python generate_invite.py
```

This will generate a Discord invite link with the required permissions. Click the link and add the bot to your server.

### Running the Bot

**Development mode:**
```bash
python run_bot.py
```

**Using uv:**
```bash
uv run soundscribe
```

### Recording a Conversation

1. Join a voice channel in Discord
2. Use `/join` command to start recording
3. Have your conversation
4. Use `/stop` command to end recording and get download link
5. Use `/last_recording` to get the download link again if needed

## Project Structure

```
soundscribe/
   src/soundscribe/
      __init__.py          # Main entry point
      bot.py               # Core bot class
      server.py            # Download server
      commands/            # Slash commands
         recording.py     # Recording commands
      audio/               # Audio processing
         recorder.py      # Recording system
         mixer.py         # Audio mixing
         sinks.py         # Custom audio sinks
      utils/               # Utilities
   recordings/              # Output directory
   docs/                    # Documentation
   pyproject.toml          # Dependencies
   run_bot.py              # Standalone runner
```

## Technical Details

- **Discord Integration**: Built with Pycord for voice recording support
- **Audio Processing**: Uses FFmpeg for professional-quality audio mixing
- **File Serving**: Embedded FastAPI server for secure downloads
- **Package Management**: Uses uv for fast dependency management

## Troubleshooting

### Common Issues

1. **"FFmpeg not found"**
   - Ensure FFmpeg is installed and available in your PATH

2. **"Bot not responding to commands"**
   - Check that the bot has the correct permissions
   - Verify the bot token is correct

3. **"No audio recorded"**
   - Ensure users are speaking and have microphones enabled
   - Check Discord voice settings

### Logs

The bot creates a `soundscribe.log` file with detailed logging information.

## Development

This project follows the iterative development approach outlined in the project documentation:

- **Phase 1 (MVP)**: Core recording and download functionality 
- **Phase 2**: AI-powered summaries (planned)
- **Phase 3**: Full transcription services (planned)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please check the documentation in the `docs/` directory or create an issue in the repository.