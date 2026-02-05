
#Step1: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY=os.getenv("ELEVENLABS_API_KEY")

#Step1: Setup Text to Speech–TTS–model with ElevenLabs
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    
    # Initialize the ElevenLabs client with your API key from the .env file
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    # Generate the audio
    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM", # Example Voice ID (Rachel). Find others in your Voice Lab.
        output_format="mp3_44100_128",
        text=input_text,
        model_id="eleven_multilingual_v2",
    )

    save(audio, output_filepath)
    print("Audio saved as output_speech.mp3")   
    
    return output_filepath

# input_text="Hi this is Ai with Samina!"
# text_to_speech_with_elevenlabs(input_text, output_filepath="../audio_records/elevenlabs_autoplay.mp3")