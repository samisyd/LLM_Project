# if you dont use pipenv uncomment the following:
# from PIL import Image
# from pathlib import Path

#VoiceBot UI with StreamLit
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from llm_brain import encode_image, analyze_image_with_query
from patient_voice import transcribe_with_groq
from doctors_voice import text_to_speech_with_elevenlabs
from utils import createDirIfNotExists

# Create a folder for saving audio files in the current directory
input_dir = createDirIfNotExists(directory_path="../audio_records/inputs")
output_dir = createDirIfNotExists(directory_path="../audio_records/outputs")
image_dir = createDirIfNotExists(directory_path="../images")

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


# The main function to process audio and image inputs, analyzes it and returns doctors response
def process_inputs(audio_filepath, image_filepath):
    try:
        # Transcribe audio to text
        try:
            speech_to_text_output = transcribe_with_groq(audio_filepath, stt_model="whisper-large-v3")
            logging.info(f"got output: {speech_to_text_output}")
        except FileNotFoundError as e:
            logging.error(f"Audio file not found: {e}")
            raise
        except Exception as e:
            logging.error(f"Error during transcription: {e}")
            raise

        # Handle the image input
        if image_filepath:
            try:
                doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct")
            except FileNotFoundError as e:
                logging.error(f"Image file not found: {e}")
                doctor_response = "Could not analyze image - file not found"
            except Exception as e:
                logging.error(f"Error analyzing image: {e}")
                doctor_response = f"Error analyzing image: {str(e)}"
        else:
            doctor_response = "No image provided for me to analyze"

        # Generate voice response
        try:
            filename = "final.mp3"
            new_audio_file_path = f"{output_dir}\\{filename}"
            logging.info(f"New audio file path: {new_audio_file_path}")
            voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=new_audio_file_path)
        except Exception as e:
            logging.error(f"Error generating voice response: {e}")
            raise

        return speech_to_text_output, doctor_response, voice_of_doctor
    except Exception as e:
        logging.error(f"Critical error in process_inputs: {e}")
        raise

# The MAIN UI starts here
st.title("AI Skin Doctor")
audio_file = st.audio_input("Record your voice and enter the problem you are facing. ")

if audio_file is not None:
    try:
        # Set the path to the current directory + file name
        # audio_file_path = f".\\audio_records\\{audio_file.name}"
        audio_file_path = input_dir / audio_file.name
        
        # Write the file to the current directory
        with open(audio_file_path, "wb") as f:
            f.write(audio_file.read())
        logging.info(f"Audio file saved successfully: {audio_file_path}")
    except IOError as e:
        logging.error(f"Error saving audio file: {e}")
        st.error(f"Failed to save audio file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error handling audio file: {e}")
        st.error(f"Unexpected error: {e}")        

if audio_file:
    st.audio(audio_file) # Plays the recorded audio back

# Upload the image file for analysis
uploaded_file = st.file_uploader("Choose an image that describes your skin condition...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    try:
        logging.info("Image uploaded")
        # Set the path to the current directory + file name    
        image_file_path = image_dir / uploaded_file.name
        logging.info(f"Image file path: {image_file_path}")
        
        # Write the file to the current directory
        with open(image_file_path, "wb") as f:
            f.write(uploaded_file.read())
        logging.info(f"Image file saved successfully: {image_file_path}")
    except IOError as e:
        logging.error(f"Error saving image file: {e}")
        st.error(f"Failed to save image file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error handling image file: {e}")
        st.error(f"Unexpected error: {e}")    
    
if audio_file and uploaded_file:
    try:
        logging.info(f"Audio file path: {audio_file_path}")
        speech_to_text_output, doctor_response, voice_of_doctor = process_inputs(audio_file_path,
                                                                                     image_file_path)

        st.subheader("Transcribed Text")
        st.write(speech_to_text_output)

        st.subheader("Doctor's Response")
        st.write(doctor_response)

        st.subheader("Voice of Doctor")
        st.audio(voice_of_doctor)

    except Exception as e:
        logging.error(f"Error processing inputs: {e}")
        st.error(f"Failed to process your audio and image: {e}")
        st.info("Please ensure both audio and image are properly uploaded and try again.")   


