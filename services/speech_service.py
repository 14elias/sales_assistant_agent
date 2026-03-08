import whisper
import tempfile


class SpeechService:

    def __init__(self):
        self.model = whisper.load_model("base")
        self.buffer = bytearray()

    def transcribe_chunk(self, audio_chunk: bytes):

        self.buffer.extend(audio_chunk)

        # save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(self.buffer)
            filename = f.name

        result = self.model.transcribe(filename)

        return result["text"]

    def is_final(self):
        """
        In a real streaming system this checks silence detection.
        For now we assume the chunk is complete.
        """
        return True



from gtts import gTTS
import uuid
import os


class TTSService:

    def __init__(self, output_dir="audio_responses"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def speak(self, text: str):

        filename = f"{uuid.uuid4()}.mp3"
        path = os.path.join(self.output_dir, filename)

        tts = gTTS(text=text, lang="en")
        tts.save(path)

        return path



speech_service = SpeechService()
tts_service = TTSService()