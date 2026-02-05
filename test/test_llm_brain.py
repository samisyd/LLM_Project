# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import os
import base64
from groq import Groq
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

#Step1: Setup GROQ API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

#Step2: Convert image to required format
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        logging.error(f"Image file '{image_path}' not found")
        raise FileNotFoundError(f"Image file '{image_path}' not found")
    except Exception as e:
        logging.error(f"Error encoding image: {e}")
        raise Exception(f"Error encoding image: {e}")

#Step3: Setup Multimodal LLM 

query="Is there something wrong with my face?"
model="meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_image_with_query(query, model, encoded_image):
    try:
        client = Groq(api_key=api_key)
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error analyzing image: {e}")
        raise Exception(f"Error analyzing image: {e}")

try:
    response = analyze_image_with_query(query, model, encode_image("acne.jpg"))    
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")