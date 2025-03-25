import os
from gtts import gTTS

class TextToSpeech:
    """Handles text-to-speech conversion."""
    
    def __init__(self, static_folder):
        self.audio_path = os.path.join(static_folder, "audio.mp3")
    
    def convert_and_save(self, text):
        """Convert text to audio and save as an MP3 file."""
        tts = gTTS(text=text, lang='en')
        tts.save(self.audio_path)
    
    def get_audio_bytes(self):
        """Retrieve audio bytes for playback."""
        if os.path.exists(self.audio_path):
            with open(self.audio_path, "rb") as audio_file:
                return audio_file.read()
        else:
            return None