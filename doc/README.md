# AI Skin Doctor - Project Documentation

## Overview

AI Skin Doctor is an interactive Streamlit-based application that combines speech recognition, computer vision, and text-to-speech technologies to provide medical advice for skin conditions. Users can record their voice describing their symptoms and upload an image of their skin condition, and the AI will analyze the information and provide a voice response.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [API Documentation](#api-documentation)
8. [Architecture](#architecture)
9. [Error Handling](#error-handling)
10. [Contributing](#contributing)

## Project Structure

```
LLMProject/
├── src/
│   ├── app.py                    # Main Streamlit application
│   ├── llm_brain.py              # Image analysis with Groq LLM
│   ├── patient_voice.py          # Speech-to-text transcription
│   ├── doctors_voice.py          # Text-to-speech generation
│   ├── utils.py                  # Utility functions
│   └── main.py                   # Entry point
├── test/                         # Test files
├── doc/                          # Documentation
├── audio_records/
│   ├── inputs/                   # User audio recordings
│   └── outputs/                  # Generated doctor responses
├── images/                       # Uploaded images
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
├── .env                         # Environment variables (not in repo)
└── README.md                    # Project overview
```

## Features

### 1. Voice Input
- Record audio through web browser
- Automatic audio format conversion (to MP3)
- Speech-to-text transcription using Groq's Whisper model

### 2. Image Analysis
- Support for JPG, JPEG, and PNG formats
- Medical image analysis using Meta's Llama 4 Scout vision model
- Base64 encoding for secure image transmission

### 3. AI Response
- Context-aware medical advice
- Natural language responses
- Differential diagnosis suggestions

### 4. Voice Output
- Text-to-speech conversion using Google Text-to-Speech (gTTS)
- Natural-sounding voice responses
- Audio playback in browser

### 5. Observability & Monitoring
- LangSmith integration for tracing and monitoring
- Function-level tracing for debugging
- Performance monitoring and analytics

## Technology Stack

### Core Technologies
- **Python 3.10+**: Programming language
- **Streamlit**: Web application framework
- **Groq API**: LLM and STT services
- **gTTS**: Google Text-to-Speech for voice generation
- **LangSmith**: Observability and tracing platform

### Key Libraries
- `groq==0.15.0`: Groq API client
- `streamlit`: Web UI framework
- `SpeechRecognition`: Audio processing
- `pydub`: Audio format conversion
- `gtts`: Google Text-to-Speech
- `python-dotenv`: Environment variable management
- `langsmith`: LangSmith SDK for observability
- `langchain`: LangChain framework support

### AI Models Used
- **Whisper Large V3**: Speech-to-text transcription
- **Llama 4 Scout 17B**: Multimodal image analysis
- **gTTS**: Google Text-to-Speech for voice synthesis

## Installation

### Prerequisites
1. Python 3.10 or higher
2. FFmpeg (for audio processing)
3. API Keys:
   - Groq API Key
   - LangSmith API Key (optional, for tracing)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LLMProject
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LANGCHAIN_TRACING_V2=your_langsmith_api_key_here
   LANGCHAIN_PROJECT=ai-skin-doctor
   ```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API authentication key | Yes | None |
| `LANGCHAIN_TRACING_V2` | LangSmith API key for tracing | No | None |
| `LANGCHAIN_PROJECT` | LangSmith project name | No | ai-skin-doctor |

### Model Configuration

Models can be configured in the respective Python files:

**llm_brain.py**:
```python
model = "meta-llama/llama-4-scout-17b-16e-instruct"
```

**patient_voice.py**:
```python
stt_model = "whisper-large-v3"
```

**doctors_voice.py**:
```python
language = "en"  # Language for gTTS
slow = False  # Speech speed
```

### System Prompt Customization

The system prompt in `app.py` can be modified to change the AI's behavior:

```python
system_prompt = """You have to act as a professional doctor..."""
```

## Usage

### Running the Application

1. **Navigate to the src directory**
   ```bash
   cd src
   ```

2. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Access the application**
   - Open your browser to `http://localhost:8501`

### User Workflow

1. **Record Audio**: Click the audio input button and describe your skin condition
2. **Upload Image**: Select an image file showing your skin condition
3. **Submit**: The app processes both inputs automatically
4. **View Results**:
   - Transcribed text of your audio
   - AI doctor's response
   - Audio playback of the response

### Example Use Case

```
User Audio: "I have red bumps on my face that are painful and won't go away"
User Image: [Photo of facial acne]

AI Response: "With what I see, I think you have inflammatory acne. 
              Try using benzoyl peroxide and consider consulting a 
              dermatologist if symptoms persist."
```

## API Documentation

### Module: llm_brain.py

#### `encode_image(image_path: str) -> str`
Encodes an image file to base64 format.

**Parameters:**
- `image_path` (str): Path to the image file

**Returns:**
- str: Base64 encoded image string

**Decorators:**
- `@traceable(run_type="tool", name="encode_image")`: LangSmith tracing

**Raises:**
- `FileNotFoundError`: If image file doesn't exist
- `Exception`: For other encoding errors

**Example:**
```python
encoded = encode_image("path/to/image.jpg")
```

#### `analyze_image_with_query(query: str, model: str, encoded_image: str) -> str`
Analyzes an image using Groq's multimodal LLM.

**Parameters:**
- `query` (str): Text prompt for analysis
- `model` (str): Model identifier
- `encoded_image` (str): Base64 encoded image

**Returns:**
- str: AI-generated analysis

**Decorators:**
- `@traceable(run_type="llm")`: LangSmith tracing for LLM calls

**Raises:**
- `Exception`: If API call fails

**Example:**
```python
response = analyze_image_with_query(
    query="What skin condition is this?",
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    encoded_image=encoded_img
)
```

### Module: patient_voice.py

#### `convert_audio_to_mp3(input_file: str) -> str`
Converts audio file to MP3 format.

**Parameters:**
- `input_file` (str): Path to input audio file

**Returns:**
- str: Path to converted MP3 file

**Raises:**
- `ValueError`: If no audio file provided
- `FileNotFoundError`: If FFmpeg not found
- `Exception`: For conversion errors

#### `transcribe_with_groq(audio_wav_file: str, stt_model: str) -> str`
Transcribes audio to text using Groq's Whisper model.

**Parameters:**
- `audio_wav_file` (str): Path to audio file
- `stt_model` (str): Model identifier

**Returns:**
- str: Transcribed text

**Raises:**
- `ValueError`: If no audio file provided
- `Exception`: For transcription errors

**Example:**
```python
text = transcribe_with_groq("audio.wav", "whisper-large-v3")
```

### Module: doctors_voice.py

#### `text_to_speech_with_gtts(input_text: str, output_filepath: str) -> str`
Converts text to speech using Google Text-to-Speech (gTTS).

**Parameters:**
- `input_text` (str): Text to convert
- `output_filepath` (str): Path to save audio file

**Returns:**
- str: Path to saved audio file

**Decorators:**
- `@traceable`: LangSmith tracing enabled

**Example:**
```python
audio_path = text_to_speech_with_gtts(
    "Hello patient",
    "output.mp3"
)
```

### Module: utils.py

#### `createDirIfNotExists(directory_path: str) -> Path`
Creates directory if it doesn't exist.

**Parameters:**
- `directory_path` (str): Path to create

**Returns:**
- Path: Path object of created directory

**Example:**
```python
from pathlib import Path
dir_path = createDirIfNotExists("audio_records/inputs")
```

### Module: app.py

#### `process_inputs(audio_filepath: str, image_filepath: str) -> tuple`
Main processing function that orchestrates the entire workflow.

**Parameters:**
- `audio_filepath` (str): Path to user's audio recording
- `image_filepath` (str): Path to uploaded image

**Returns:**
- tuple: (transcribed_text, doctor_response, audio_response_path)

**Raises:**
- `FileNotFoundError`: If files not found
- `Exception`: For processing errors

## Architecture

### System Flow

```
User Input (Audio + Image)
    ↓
[Streamlit UI (app.py)]
    ↓
[File Storage] → audio_records/inputs/, images/
    ↓
[Audio Processing] → patient_voice.py
    ├── Format Conversion (MP3)
    └── Speech-to-Text (Groq Whisper)
    ↓
[Image Processing] → llm_brain.py
    ├── Base64 Encoding
    └── Image Analysis (Llama 4 Scout)
    ↓
[Response Generation] → doctors_voice.py
    └── Text-to-Speech (ElevenLabs)
    ↓
[Output Storage] → audio_records/outputs/
    ↓
[Display Results] → Streamlit UI
```

### Data Flow

1. **Input Phase**:
   - User records audio via browser
   - User uploads image file
   - Files saved to local storage

2. **Processing Phase**:
   - Audio converted to MP3
   - Audio transcribed to text
   - Image encoded to base64
   - Combined query sent to Llama model

3. **Response Phase**:
   - AI generates text response
   - Text converted to speech using gTTS
   - Audio file saved
   - All operations traced via LangSmith

4. **Output Phase**:
   - Display transcription
   - Display AI response
   - Play audio response

## Error Handling

### Exception Types

The application implements comprehensive error handling:

1. **File Errors**:
   ```python
   FileNotFoundError: Missing audio/image files
   IOError: File read/write errors
   ```

2. **API Errors**:
   ```python
   ValueError: Missing API keys
   Exception: API request failures
   ```

3. **Processing Errors**:
   ```python
   Exception: Transcription/analysis failures
   ```

### Error Recovery

- **Missing Files**: User-friendly error messages displayed in UI
- **API Failures**: Logged with detailed error messages
- **Processing Errors**: Graceful degradation with informative feedback

### Logging

The application uses Python's logging module:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

**Log Levels**:
- `INFO`: Normal operation events
- `ERROR`: Error conditions

**Log Locations**:
- Console output (stdout/stderr)
- Can be configured to file output

## Best Practices

### For Developers

1. **API Keys**: Never commit `.env` file to version control
2. **Testing**: Test audio/image inputs before deployment
3. **Error Handling**: Always wrap API calls in try-except blocks
4. **Logging**: Use appropriate log levels
5. **Path Handling**: Use Path objects for cross-platform compatibility

### For Users

1. **Audio Quality**: Record in quiet environment
2. **Image Quality**: Use clear, well-lit photos
3. **File Formats**: Use supported formats (MP3, WAV for audio; JPG, PNG for images)
4. **Privacy**: Don't share real medical images without consent

## Troubleshooting

### Common Issues

**1. FFmpeg Not Found**
```
Error: FFmpeg or the input file was not found
Solution: Install FFmpeg and add to system PATH
```

**2. API Key Missing**
```
ValueError: GROQ_API_KEY not found in environment variables
Solution: Create .env file with valid API keys
```

**5. LangSmith Tracing Issues**
```
Warning: LANGCHAIN_TRACING_V2 not found
Solution: Optional - add LangSmith API key for tracing functionality
```

**3. Audio Recording Issues**
```
Solution: Check browser permissions for microphone access
```

**4. Image Upload Fails**
```
Solution: Ensure file size < 200MB and correct format
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where appropriate
- Write descriptive commit messages

## License

This project is for educational purposes. Consult license file for details.

## Disclaimer

⚠️ **Medical Disclaimer**: This application is for educational purposes only and should not replace professional medical advice. Always consult with qualified healthcare providers for medical concerns.

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review error logs

---

**Last Updated**: February 2026
**Version**: 1.0.0
