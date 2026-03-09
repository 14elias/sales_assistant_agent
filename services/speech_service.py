import os
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import ListenV1Results, ListenV1Metadata

logger = logging.getLogger(__name__)

load_dotenv()


class SpeechService:
    """
    Production-grade streaming Speech-to-Text service using Deepgram v6.
    """

    def __init__(self):
        api_key = os.getenv("DEEPGRAM_API_KEY2")
        if not api_key:
            raise RuntimeError("DEEPGRAM_API_KEY environment variable not set")

        self.client = AsyncDeepgramClient(api_key=api_key)

        self.connection = None
        self._connection_ctx = None

        self._final_transcript: Optional[str] = None
        self._partial_transcript: Optional[str] = None
        self._speech_final = False

        self._lock = asyncio.Lock()

    async def connect(self):
        """Initialize Deepgram streaming connection."""

        options = {
            "model": "nova-3",
            "language": "en-US",
        }

        # Open websocket connection
        self._connection_ctx = self.client.listen.v1.connect(**options)
        self.connection = await self._connection_ctx.__aenter__()

        # Register event handlers
        self.connection.on(EventType.OPEN, lambda _: logger.info("Deepgram connection opened"))
        self.connection.on(EventType.MESSAGE, self._on_message)
        self.connection.on(EventType.ERROR, lambda e: logger.error(f"Deepgram Error: {e}"))
        self.connection.on(EventType.CLOSE, lambda _: logger.info("Deepgram connection closed"))

        # Start listener task
        await self.connection.start_listening()

        logger.info("Deepgram streaming connection started")

    async def send_audio(self, audio_chunk: bytes):
        """Send audio chunk to Deepgram."""
        if not self.connection:
            raise RuntimeError("SpeechService not connected")

        try:
            await self.connection.send_media(audio_chunk)
        except Exception:
            logger.exception("Error sending audio chunk to Deepgram")
            raise

    async def _on_message(self, message, **kwargs):
        """Handle Deepgram websocket messages."""

        try:
            # Metadata messages
            if isinstance(message, ListenV1Metadata):
                logger.debug("Received metadata event")
                return

            # Transcript messages
            if isinstance(message, ListenV1Results):

                channel = message.channel
                if not channel or not channel.alternatives:
                    return

                transcript = channel.alternatives[0].transcript
                if not transcript:
                    return

                async with self._lock:
                    if message.is_final:
                        self._final_transcript = transcript
                        self._speech_final = True
                        logger.debug("Final transcript: %s", transcript)
                    else:
                        self._partial_transcript = transcript

        except Exception:
            logger.exception("Error processing Deepgram message")

    async def get_final_transcript(self) -> Optional[str]:
        """Return final transcript when speech is completed."""

        async with self._lock:
            if not self._speech_final:
                return None

            text = self._final_transcript
            self._final_transcript = None
            self._speech_final = False

            return text

    async def send_keep_alive(self):
        """Send keep-alive signal to prevent timeout."""

        if self.connection:
            await self.connection.send_keep_alive()

    async def finalize(self):
        """Tell Deepgram the audio stream has finished."""

        if self.connection:
            await self.connection.send_finalize()

    async def close(self):
        """Close Deepgram connection cleanly."""

        if self.connection:
            try:
                await self.connection.send_close_stream()
                await self.connection.close()
            finally:
                if self._connection_ctx:
                    await self._connection_ctx.__aexit__(None, None, None)

            logger.info("Deepgram connection closed")


import uuid
from pathlib import Path
from elevenlabs.client import ElevenLabs



class TTSService:
    """
    Production-grade Text-to-Speech service using ElevenLabs.

    Features:
    - configurable voices
    - streaming audio generation
    - fault-tolerant synthesis
    - file-based audio caching
    """

    def __init__(
        self,
        output_dir: str = "audio_responses",
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        model_id: str = "eleven_multilingual_v2",
    ):

        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise RuntimeError("ELEVENLABS_API_KEY environment variable not set")

        self.client = ElevenLabs(api_key=api_key)

        self.voice_id = voice_id
        self.model_id = model_id

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def speak(self, text: str) -> str:
        """
        Convert text to speech and store audio file.

        Returns path to generated audio file.
        """

        if not text:
            raise ValueError("Text for TTS cannot be empty")

        filename = f"{uuid.uuid4()}.mp3"
        path = self.output_dir / filename

        try:

            audio_stream = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                model_id=self.model_id,
                text=text,
                output_format="mp3_44100_128"
            )

            with open(path, "wb") as f:
                for chunk in audio_stream:
                    if chunk:
                        f.write(chunk)

            logger.debug("TTS audio generated: %s", path)

            return str(path)

        except Exception as e:
            logger.exception("ElevenLabs synthesis failed")
            raise e
        
speech_service = SpeechService()
tts_service = TTSService()


# --- TEST BLOCK ---
async def main():
    # 1. Test ElevenLabs (Synchronous method)
    # tts = TTSService()
    # audio_path = tts.speak("Hello, the sales assistant agent is ready.")
    # print(f"ElevenLabs Result: {audio_path}")

    # 2. Test Deepgram Connection (Asynchronous)
    speech = SpeechService()
    try:
        await speech.connect()
        print("Deepgram connection successful!")
        # Since we don't have a mic stream here, we close it immediately
        await speech.close()
    except Exception as e:
        print(f"Deepgram Connection failed: {e}")

if __name__ == '__main__':
    asyncio.run(main())