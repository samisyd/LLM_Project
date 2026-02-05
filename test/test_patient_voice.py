
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


#Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
import logging
from pydub import AudioSegment
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1 - Convert audio to wav format
def convert_audio_to_mp3(input_file) : # timeout=20, phrase_time_limit=None):
    """
    Converts an audio file to MP3 format using pydub.
    Ensure FFmpeg is installed and accessible in the system's PATH.
    """
    try:

        if input_file:
            print("Audio file provided:", input_file)
            current_directory = Path.cwd()
            input_path = Path(input_file)
            new_audio_file_path = (current_directory / input_path).resolve()
            print("Audio file provided:", new_audio_file_path)
            logging.info("Audio file provided")
        else:
            logging.info("No audio file provided.")
            raise ValueError("Audio file is required.")

        # Determine the format from the input file extension
        input_format = new_audio_file_path.suffix.strip('.').lower()
        audio_file_name = new_audio_file_path.stem
        logging.info(f"Input format detected: {input_format}") 
        logging.info(f"Audio file name: {audio_file_name}")
        
        # Load the audio file
        audio = AudioSegment.from_file(new_audio_file_path, format=input_format)
        output_dir = (current_directory / ".." / "audio_records").resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filename = output_dir / f"{audio_file_name}_audio.mp3"        
        # Export the audio file to MP3 format
        audio.export(output_filename, format="mp3")        
        logging.info(f"Successfully converted {input_file} to {output_filename}")        
        return output_filename       
        
    except FileNotFoundError:
        logging.error("Error: FFmpeg or the input file was not found.")
        logging.error("Please ensure FFmpeg is installed and added to your system's PATH, and the input file path is correct.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")    

#Step2: Setup Speech to text–STT–model for transcription
import os
from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"

def transcribe_with_groq(audio_wav_file, stt_model):

    try:        
        client=Groq(api_key=GROQ_API_KEY)

        if audio_wav_file:
            print("Audio file provided:")
        else:
            print("No audio file provided.")
            raise ValueError("Audio file is required.")
            
        audio_filepath = convert_audio_to_mp3(audio_wav_file)
        
        audio_file=open(audio_filepath, "rb")
        transcription=client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None

    return transcription.text

response = transcribe_with_groq("2026-02-03T21-04_audio.wav", "whisper-large-v3")
print(response)