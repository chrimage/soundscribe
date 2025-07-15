"""FastAPI embedded web server for secure file downloads."""

import asyncio
import logging
import secrets
import time
from typing import Dict, Optional
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)


class DownloadServer:
    """Embedded web server for secure file downloads."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.host = host
        self.port = port
        self.app = FastAPI(title="SoundScribe Download Server")
        self.server: Optional[uvicorn.Server] = None
        self.server_task: Optional[asyncio.Task] = None
        
        # Token storage: token -> (file_path, expiry_time)
        self.download_tokens: Dict[str, tuple[str, float]] = {}
        
        # Token expiry time (1 hour)
        self.token_expiry = 3600
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up FastAPI routes."""
        
        @self.app.get("/")
        async def root():
            return {"message": "SoundScribe Download Server"}
        
        @self.app.get("/download/{token}")
        async def download_file(token: str):
            """Download a file using a secure token."""
            current_time = time.time()
            
            # Check if token exists
            if token not in self.download_tokens:
                raise HTTPException(status_code=404, detail="Invalid or expired download link")
            
            file_path, expiry_time = self.download_tokens[token]
            
            # Check if token has expired
            if current_time > expiry_time:
                del self.download_tokens[token]
                raise HTTPException(status_code=404, detail="Download link has expired")
            
            # Check if file exists
            if not Path(file_path).exists():
                del self.download_tokens[token]
                raise HTTPException(status_code=404, detail="File not found")
            
            # Return the file
            filename = Path(file_path).name
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type="audio/mpeg"
            )
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "active_tokens": len(self.download_tokens)}
    
    async def start(self):
        """Start the download server."""
        if self.server_task:
            return  # Already running
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="warning",  # Reduce uvicorn logging
            access_log=False
        )
        
        self.server = uvicorn.Server(config)
        self.server_task = asyncio.create_task(self.server.serve())
        
        # Wait a moment for the server to start
        await asyncio.sleep(0.1)
        logger.info(f"Download server started on http://{self.host}:{self.port}")
    
    async def stop(self):
        """Stop the download server."""
        if self.server:
            self.server.should_exit = True
            
        if self.server_task:
            try:
                await asyncio.wait_for(self.server_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Server shutdown timed out")
                self.server_task.cancel()
            finally:
                self.server_task = None
                self.server = None
        
        logger.info("Download server stopped")
    
    async def create_download_link(self, file_path: str) -> str:
        """Create a secure download link for a file."""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expiry_time = time.time() + self.token_expiry
        
        # Store token
        self.download_tokens[token] = (file_path, expiry_time)
        
        # Clean up expired tokens
        await self._cleanup_expired_tokens()
        
        download_url = f"http://{self.host}:{self.port}/download/{token}"
        logger.debug(f"Created download link: {download_url}")
        
        return download_url
    
    async def _cleanup_expired_tokens(self):
        """Remove expired tokens."""
        current_time = time.time()
        expired_tokens = [
            token for token, (_, expiry) in self.download_tokens.items()
            if current_time > expiry
        ]
        
        for token in expired_tokens:
            del self.download_tokens[token]
        
        if expired_tokens:
            logger.debug(f"Cleaned up {len(expired_tokens)} expired tokens")