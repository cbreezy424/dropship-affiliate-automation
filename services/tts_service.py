import os
from gtts import gTTS
from app.utils import ensure_directory, generate_unique_filename

class TTSService:
    """Text-to-Speech service using Google Translate API (gTTS)"""
    
    def __init__(self):
        self.output_folder = os.getenv('TEMP_FOLDER', 'temp')
        ensure_directory(self.output_folder)
    
    def text_to_speech(self, text, language='en', output_filename=None, slow=False):
        """
        Convert text to speech using gTTS
        
        Args:
            text: Text to convert to speech
            language: Language code (en, es, fr, etc.)
            output_filename: Custom output filename
            slow: Slow down speech
        
        Returns:
            Path to generated audio file
        """
        
        try:
            if output_filename is None:
                output_filename = generate_unique_filename('audio.mp3')
            
            output_path = os.path.join(self.output_folder, output_filename)
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to file
            tts.save(output_path)
            
            print(f"TTS saved to: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            raise
    
    def batch_text_to_speech(self, texts, language='en'):
        """
        Convert multiple texts to speech
        
        Args:
            texts: List of texts to convert
            language: Language code
        
        Returns:
            List of audio file paths
        """
        
        audio_files = []
        for text in texts:
            try:
                audio_path = self.text_to_speech(text, language)
                audio_files.append(audio_path)
            except Exception as e:
                print(f"Error converting text to speech: {str(e)}")
                continue
        
        return audio_files
