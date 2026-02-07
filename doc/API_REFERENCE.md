# API Reference Guide

## Overview

This document provides detailed technical documentation for all modules, functions, and classes in the AI Skin Doctor project.

---

## Table of Contents

1. [llm_brain Module](#llm_brain-module)
2. [patient_voice Module](#patient_voice-module)
3. [doctors_voice Module](#doctors_voice-module)
4. [app Module](#app-module)
5. [utils Module](#utils-module)
6. [Error Codes](#error-codes)

---

## llm_brain Module

**File**: `src/llm_brain.py`

**Purpose**: Handles image encoding and multimodal LLM analysis using Groq API.

### Dependencies

```python
import os
import base64
from groq import Groq
from dotenv import load_dotenv
import logging
from langsmith import traceable
```

### Global Variables

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `api_key` | str | Groq API authentication key | From environment |
| `query` | str | Default query for testing | "Is there something wrong with my face?" |
| `model` | str | LLM model identifier | "meta-llama/llama-4-scout-17b-16e-instruct" |

### Functions

#### `encode_image(image_path: str) -> str`

Encodes an image file to base64 format for API transmission.

**Decorators:**
- `@traceable(run_type="tool", name="encode_image")`: LangSmith tracing for debugging

**Parameters:**
- `image_path` (str): Absolute or relative path to the image file

**Returns:**
- `str`: Base64 encoded string of the image

**Raises:**
- `FileNotFoundError`: When the specified image file doesn't exist
- `Exception`: For any other encoding errors (e.g., corrupt file, permission issues)

**Example Usage:**
```python
from llm_brain import encode_image

# Encode image
encoded_img = encode_image("path/to/image.jpg")
print(f"Encoded length: {len(encoded_img)}")
```

**Implementation Details:**
- Opens file in binary read mode
- Uses base64.b64encode for encoding
- Decodes bytes to UTF-8 string
- Logs errors with detailed messages

---

#### `analyze_image_with_query(query: str, model: str, encoded_image: str) -> str`

Sends an image and text query to Groq's multimodal LLM for analysis.

**Decorators:**
- `@traceable(run_type="llm")`: LangSmith tracing for LLM calls and monitoring

**Parameters:**
- `query` (str): Text prompt or question about the image
- `model` (str): Model identifier (e.g., "meta-llama/llama-4-scout-17b-16e-instruct")
- `encoded_image` (str): Base64 encoded image string

**Returns:**
- `str`: AI-generated text response analyzing the image

**Raises:**
- `Exception`: For API communication errors, invalid model, or rate limiting

**Example Usage:**
```python
from llm_brain import analyze_image_with_query, encode_image

encoded = encode_image("skin_condition.jpg")
response = analyze_image_with_query(
    query="What skin condition does this image show?",
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    encoded_image=encoded
)
print(response)
```

**API Request Format:**
```python
{
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ],
    "model": model
}
```

**Response Format:**
```python
# Returns the content field from:
chat_completion.choices[0].message.content
```

---

## patient_voice Module

**File**: `src/patient_voice.py`

**Purpose**: Handles audio recording, format conversion, and speech-to-text transcription.

### Dependencies

```python
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pathlib import Path
from groq import Groq
import logging
```

### Global Variables

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `GROQ_API_KEY` | str | API key for Groq services | From environment |
| `stt_model` | str | Speech-to-text model | "whisper-large-v3" |

### Functions

#### `convert_audio_to_mp3(input_file: str) -> str`

Converts audio files to MP3 format using pydub and FFmpeg.

**Parameters:**
- `input_file` (str): Path to input audio file (any format supported by FFmpeg)

**Returns:**
- `str`: Path to the converted MP3 file

**Raises:**
- `ValueError`: If input_file is None or empty
- `FileNotFoundError`: If FFmpeg is not installed or input file doesn't exist
- `Exception`: For conversion errors

**Supported Input Formats:**
- WAV, MP3, FLAC, OGG, M4A, WMA, AAC, etc.

**Example Usage:**
```python
from patient_voice import convert_audio_to_mp3

# Convert WAV to MP3
mp3_path = convert_audio_to_mp3("recording.wav")
print(f"Converted file saved at: {mp3_path}")
```

**Implementation Details:**
- Automatically detects input format from file extension
- Extracts base filename without extension
- Saves output to `../audio_records/{filename}_audio.mp3`
- Logs all operations and errors

**Output Path Format:**
```
../audio_records/{original_filename}_audio.mp3
```

---

#### `transcribe_with_groq(audio_wav_file: str, stt_model: str) -> str`

Transcribes audio file to text using Groq's Whisper model.

**Parameters:**
- `audio_wav_file` (str): Path to audio file (any format)
- `stt_model` (str): Model identifier (e.g., "whisper-large-v3")

**Returns:**
- `str`: Transcribed text from the audio
- `None`: If an error occurs during transcription

**Raises:**
- `ValueError`: If audio file path is not provided
- `Exception`: For API errors or transcription failures

**Example Usage:**
```python
from patient_voice import transcribe_with_groq

# Transcribe audio
text = transcribe_with_groq(
    audio_wav_file="user_recording.wav",
    stt_model="whisper-large-v3"
)
print(f"Transcription: {text}")
```

**Process Flow:**
1. Validates audio file exists
2. Converts to MP3 format
3. Opens converted file in binary mode
4. Sends to Groq API for transcription
5. Returns transcribed text

**API Configuration:**
```python
client.audio.transcriptions.create(
    model=stt_model,
    file=audio_file,
    language="en"  # Fixed to English
)
```

---

## doctors_voice Module

**File**: `src/doctors_voice.py`

**Purpose**: Converts text responses to natural-sounding speech using Google Text-to-Speech (gTTS).

### Dependencies

```python
from gtts import gTTS
from langsmith import traceable
```

### Global Variables

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `language` | str | Language code for speech | "en" |
| `slow` | bool | Speech speed | False |

### Functions

#### `text_to_speech_with_gtts(input_text: str, output_filepath: str) -> str`

Converts text to speech using Google Text-to-Speech (gTTS).

**Decorators:**
- `@traceable`: LangSmith tracing for TTS operations

**Parameters:**
- `input_text` (str): Text content to convert to speech
- `output_filepath` (str): Path where the audio file will be saved

**Returns:**
- `str`: Path to the saved audio file

**Raises:**
- `Exception`: For file write errors or gTTS errors

**Example Usage:**
```python
from doctors_voice import text_to_speech_with_gtts

response_text = "You appear to have mild dermatitis."
audio_path = text_to_speech_with_gtts(
    input_text=response_text,
    output_filepath="response.mp3"
)
print(f"Audio saved to: {audio_path}")
```

**Configuration:**

| Parameter | Value | Description |
|-----------|-------|-------------|
| `language` | "en" | English language |
| `slow` | False | Normal speech speed |

**Audio Specifications:**
- Format: MP3
- Quality: Standard gTTS quality
- Free and no API key required

---

## app Module

**File**: `src/app.py`

**Purpose**: Main Streamlit application for user interface and workflow orchestration.

### Dependencies

```python
import streamlit as st
import logging
from llm_brain import encode_image, analyze_image_with_query
from patient_voice import transcribe_with_groq
from doctors_voice import text_to_speech_with_gtts
from utils import createDirIfNotExists
```

### Global Variables

| Variable | Type | Description | Value |
|----------|------|-------------|-------|
| `input_dir` | Path | Directory for audio inputs | "../audio_records/inputs" |
| `output_dir` | Path | Directory for audio outputs | "../audio_records/outputs" |
| `image_dir` | Path | Directory for images | "../images" |
| `system_prompt` | str | AI behavior instructions | Custom medical prompt |

### System Prompt

```python
system_prompt = """You have to act as a professional doctor, i know you are not 
but this is for learning purpose. What's in this image?. Do you find anything 
wrong with it medically? If you make a differential, suggest some remedies for 
them. Do not add any numbers or special characters in your response. Your response 
should be in one long paragraph. Also always answer as if you are answering to a 
real person. Do not say 'In the image I see' but say 'With what I see, I think 
you have ....' Do not respond as an AI model in markdown, your answer should mimic 
that of an actual doctor not an AI bot, Keep your answer concise (max 2 sentences). 
No preamble, start your answer right away please"""
```

### Functions

#### `process_inputs(audio_filepath: str, image_filepath: str) -> tuple`

Main processing pipeline that coordinates all operations.

**Parameters:**
- `audio_filepath` (str): Path to user's audio recording
- `image_filepath` (str): Path to uploaded image file

**Returns:**
- `tuple`: (speech_to_text_output, doctor_response, voice_of_doctor)
  - `speech_to_text_output` (str): Transcribed text from audio
  - `doctor_response` (str): AI-generated medical response
  - `voice_of_doctor` (str): Path to audio response file

**Raises:**
- `FileNotFoundError`: If audio or image files are missing
- `Exception`: For processing errors at any stage

**Example Usage:**
```python
# Internal function - called by Streamlit UI
text, response, audio = process_inputs(
    audio_filepath="inputs/recording.wav",
    image_filepath="images/skin.jpg"
)
```

**Process Flow:**

```
1. Transcribe Audio
   ├── Convert format if needed
   └── Extract text using Whisper

2. Analyze Image
   ├── Encode to base64
   ├── Combine with system prompt + user text
   └── Send to Llama 4 Scout

3. Generate Voice Response
   ├── Convert text to speech
   └── Save to outputs directory

4. Return Results
   └── (transcription, response, audio_path)
```

**Error Handling:**
- Transcription errors: Logged and raised
- Image analysis errors: Graceful fallback message
- Voice generation errors: Logged and raised
- All errors logged with detailed context

---

### Streamlit UI Components

#### Audio Input
```python
audio_file = st.audio_input("Record your voice and enter the problem you are facing.")
```
- Captures audio through browser
- Automatically saved to inputs directory
- Displays recording for playback

#### Image Upload
```python
uploaded_file = st.file_uploader(
    "Choose an image that describes your skin condition...",
    type=["jpg", "jpeg", "png"]
)
```
- Accepts common image formats
- Validates file type
- Saves to images directory

#### Results Display
- **Transcribed Text**: Shows what the user said
- **Doctor's Response**: AI-generated analysis
- **Voice of Doctor**: Audio playback of response

---

## utils Module

**File**: `src/utils.py`

**Purpose**: Utility functions for common operations.

### Dependencies

```python
from pathlib import Path
```

### Functions

#### `createDirIfNotExists(directory_path: str) -> Path`

Creates a directory if it doesn't exist, with error handling.

**Parameters:**
- `directory_path` (str): Relative or absolute path to create

**Returns:**
- `Path`: Path object representing the created/existing directory

**Raises:**
- `OSError`: If directory creation fails (logs error but continues)

**Example Usage:**
```python
from utils import createDirIfNotExists

# Create directory
audio_dir = createDirIfNotExists("audio_records/inputs")
print(f"Directory ready at: {audio_dir}")

# Use with Path operations
from pathlib import Path
file_path = audio_dir / "recording.mp3"
```

**Features:**
- Creates parent directories automatically
- Doesn't fail if directory exists
- Returns absolute path
- Cross-platform compatible
- Handles permission errors gracefully

**Implementation:**
```python
1. Get current working directory
2. Construct full path
3. Attempt to create directory
4. If fails, try with parents=True
5. Return Path object
```

---

## Error Codes

### Common Exceptions

| Error Type | Module | Cause | Solution |
|-----------|--------|-------|----------|
| `ValueError: GROQ_API_KEY not found` | llm_brain | Missing API key | Add to .env file |
| `ValueError: LANGCHAIN_TRACING_V2 not found` | llm_brain | Missing LangSmith key (optional) | Add to .env or ignore if not using tracing |
| `FileNotFoundError` | llm_brain | Image not found | Check file path |
| `Exception: Error encoding image` | llm_brain | Corrupt file | Verify image integrity |
| `FileNotFoundError: FFmpeg not found` | patient_voice | FFmpeg not installed | Install FFmpeg |
| `ValueError: Audio file is required` | patient_voice | No file provided | Check file path |
| `Exception: transcription error` | patient_voice | API failure | Check API key/quota |
| `Exception: gTTS error` | doctors_voice | TTS generation failed | Check internet connection |
| `IOError` | app | File write error | Check permissions |
| `OSError` | utils | Directory creation | Check permissions |

### HTTP Status Codes (API)

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Continue |
| 401 | Unauthorized | Check API key |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Contact support |

---

## Data Types

### AudioFile
```python
{
    "name": str,          # Filename
    "data": bytes,        # File content
    "format": str,        # Audio format (mp3, wav, etc.)
    "path": str           # Full file path
}
```

### ImageFile
```python
{
    "name": str,          # Filename
    "data": bytes,        # File content
    "format": str,        # Image format (jpg, png)
    "encoded": str,       # Base64 encoded string
    "path": str           # Full file path
}
```

### TranscriptionResponse
```python
{
    "text": str,          # Transcribed text
    "language": str,      # Detected language
    "duration": float     # Audio duration (seconds)
}
```

### AnalysisResponse
```python
{
    "content": str,       # AI response text
    "model": str,         # Model used
    "tokens": int         # Tokens consumed
}
```

---

## Configuration Files

### .env Format
```env
# Required
GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# Optional - LangSmith Tracing
LANGCHAIN_TRACING_V2=xxxxxxxxxxxxx
LANGCHAIN_PROJECT=ai-skin-doctor

# Optional (for future use)
LOG_LEVEL=INFO
MAX_AUDIO_SIZE=10485760  # 10MB in bytes
```

### requirements.txt
```txt
python-dotenv
groq==0.15.0; python_version >= '3.8'
gtts
SpeechRecognition
streamlit
uvicorn
pydub
dotenv
langchain
langsmith
```

---

## Best Practices

### API Usage

1. **Rate Limiting**: Implement exponential backoff
2. **Error Handling**: Always wrap API calls in try-except
3. **Logging**: Log all API requests and responses
4. **Timeouts**: Set appropriate timeout values

### File Handling

1. **Path Operations**: Use `pathlib.Path` for cross-platform compatibility
2. **File Cleanup**: Delete temporary files after processing
3. **Error Recovery**: Handle file I/O errors gracefully
4. **Validation**: Verify file formats before processing

### Security

1. **API Keys**: Never commit to version control
2. **Input Validation**: Sanitize all user inputs
3. **File Uploads**: Limit file sizes and types
4. **Error Messages**: Don't expose sensitive information

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Initial release |

---

## Support

For detailed implementation questions, refer to the source code or contact the development team.

**Documentation Last Updated**: February 2026
