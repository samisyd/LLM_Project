
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )    
    audioobj.save(output_filepath)
    return output_filepath

# input_text="Hi this is Ai with Samina!"
# text_to_speech_with_gtts(input_text, output_filepath="gtts_autoplay.mp3")