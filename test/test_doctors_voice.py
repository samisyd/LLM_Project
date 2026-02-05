#Step1: Setup Text to Speech–TTS–model with gTTS
# import os

# from dotenv import load_dotenv
# load_dotenv()

# ELEVENLABS_API_KEY=os.getenv("ELEVENLABS_API_KEY")

# #Step1: Setup Text to Speech–TTS–model with ElevenLabs
# from elevenlabs.client import ElevenLabs
# from elevenlabs import save

# import subprocess
# import platform

# def text_to_speech_with_elevenlabs(input_text, output_filepath):
    
#     # Initialize the ElevenLabs client with your API key from the .env file
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     # Generate the audio
#     audio = client.text_to_speech.convert(
#         voice_id="21m00Tcm4TlvDq8ikWAM", # Example Voice ID (Rachel). Find others in your Voice Lab.
#         output_format="mp3_44100_128",
#         text=input_text,
#         model_id="eleven_multilingual_v2",
#     )

#     save(audio, output_filepath)
#     print("Audio saved as output_speech.mp3")

#     print("Playing the audio...")
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             #subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
#             subprocess.run(f'start "" "{output_filepath}"', shell=True)
#             print(f"Opened {output_filepath} with the default media player.")
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")
    
#     return output_filepath

# input_text="Hi this is Ai with Samina!"
# text_to_speech_with_elevenlabs(input_text, output_filepath="../audio_records/elevenlabs_autoplay.mp3")

from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )    
    audioobj.save(output_filepath)

input_text="Hi this is Ai with Samina!"
text_to_speech_with_gtts(input_text, output_filepath="gtts_autoplay.mp3")