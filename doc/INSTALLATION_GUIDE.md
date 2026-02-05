# Installation Guide - AI Skin Doctor

Complete step-by-step installation guide for Windows, macOS, and Linux.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB free space
- **Internet**: Stable connection for API calls

### Software Dependencies

- Python 3.10+
- pip (Python package manager)
- FFmpeg (audio processing)
- Git (optional, for cloning repository)

### API Requirements

You'll need to obtain API keys from:
1. **Groq** - [https://console.groq.com](https://console.groq.com)
2. **ElevenLabs** - [https://elevenlabs.io](https://elevenlabs.io)

---

## Windows Installation

### Step 1: Install Python

1. **Download Python**
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.10 or higher
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Installation**
   ```powershell
   python --version
   # Should output: Python 3.10.x or higher
   
   pip --version
   # Should output pip version
   ```

### Step 2: Install FFmpeg

**Option A: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; 
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; 
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Open System Properties → Environment Variables
   - Edit "Path" variable
   - Add `C:\ffmpeg\bin`
   - Restart terminal

**Verify FFmpeg**
```powershell
ffmpeg -version
```

### Step 3: Clone or Download Project

**Option A: Using Git**
```powershell
# Install Git if needed
choco install git

# Clone repository
git clone <repository-url>
cd LLMProject
```

**Option B: Download ZIP**
1. Download project ZIP file
2. Extract to desired location
3. Open PowerShell in project directory

### Step 4: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Your prompt should now show (venv)
```

### Step 5: Install Python Packages

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# This may take several minutes
```

### Step 6: Configure Environment Variables

1. **Create .env file**
   ```powershell
   # In project root directory
   New-Item .env -ItemType File
   notepad .env
   ```

2. **Add API keys**
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

3. **Save and close**

### Step 7: Run the Application

```powershell
# Navigate to src directory
cd src

# Run Streamlit app
streamlit run app.py

# Browser should open automatically to http://localhost:8501
```

---

## macOS Installation

### Step 1: Install Homebrew

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

```bash
# Install Python 3.10+
brew install python@3.10

# Verify installation
python3 --version
pip3 --version
```

### Step 3: Install FFmpeg

```bash
# Install FFmpeg
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### Step 4: Clone Project

```bash
# Install Git if needed
brew install git

# Clone repository
git clone <repository-url>
cd LLMProject
```

### Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
```

### Step 6: Install Python Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 7: Configure Environment

```bash
# Create .env file
touch .env

# Edit with your preferred editor
nano .env
# or
open -e .env
```

Add:
```env
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### Step 8: Run Application

```bash
# Navigate to src
cd src

# Run application
streamlit run app.py
```

---

## Linux Installation

### Step 1: Update System

```bash
# Ubuntu/Debian
sudo apt update
sudo apt upgrade -y

# Fedora
sudo dnf update -y

# Arch
sudo pacman -Syu
```

### Step 2: Install Python

```bash
# Ubuntu/Debian
sudo apt install python3.10 python3-pip python3-venv -y

# Fedora
sudo dnf install python3.10 python3-pip -y

# Arch
sudo pacman -S python python-pip

# Verify
python3 --version
pip3 --version
```

### Step 3: Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg -y

# Fedora
sudo dnf install ffmpeg -y

# Arch
sudo pacman -S ffmpeg

# Verify
ffmpeg -version
```

### Step 4: Clone Project

```bash
# Install Git
sudo apt install git -y  # Ubuntu/Debian
sudo dnf install git -y  # Fedora
sudo pacman -S git       # Arch

# Clone repository
git clone <repository-url>
cd LLMProject
```

### Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 6: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 7: Configure Environment

```bash
# Create .env file
nano .env
```

Add:
```env
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

Save: `Ctrl+O`, Exit: `Ctrl+X`

### Step 8: Run Application

```bash
cd src
streamlit run app.py
```

---

## Verification

### Test Installation

1. **Verify Python Packages**
   ```bash
   pip list | grep -E "groq|streamlit|elevenlabs|pydub"
   ```

2. **Test FFmpeg**
   ```bash
   ffmpeg -version
   ```

3. **Check Environment Variables**
   ```python
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Groq:', 'Found' if os.getenv('GROQ_API_KEY') else 'Not Found')"
   ```

### Test Individual Components

**Test Image Encoding:**
```bash
cd src
python -c "from llm_brain import encode_image; print('Image encoding works!')"
```

**Test Audio Processing:**
```bash
python -c "from patient_voice import convert_audio_to_mp3; print('Audio processing ready!')"
```

**Test Text-to-Speech:**
```bash
python -c "from doctors_voice import text_to_speech_with_elevenlabs; print('TTS ready!')"
```

---

## Troubleshooting

### Common Issues

#### 1. Python Not Found

**Windows:**
```powershell
# Reinstall Python and ensure "Add to PATH" is checked
# Or manually add to PATH:
# C:\Python310\
# C:\Python310\Scripts\
```

**Mac/Linux:**
```bash
# Use python3 explicitly
python3 --version
# Create alias (add to ~/.bashrc or ~/.zshrc)
alias python=python3
alias pip=pip3
```

#### 2. FFmpeg Not Found

**Windows:**
```powershell
# Check PATH
echo $env:PATH | Select-String ffmpeg

# If not found, add manually or reinstall
```

**Mac:**
```bash
# Reinstall
brew reinstall ffmpeg

# Check path
which ffmpeg
```

**Linux:**
```bash
# Verify installation
dpkg -l | grep ffmpeg  # Debian/Ubuntu
rpm -qa | grep ffmpeg  # Fedora

# Reinstall if needed
sudo apt install --reinstall ffmpeg
```

#### 3. pip Install Fails

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Use specific package versions
pip install groq==0.15.0

# Install with verbose output
pip install -v package_name
```

#### 4. Permission Errors

**Windows:**
```powershell
# Run PowerShell as Administrator
```

**Mac/Linux:**
```bash
# Don't use sudo with pip in virtual environment
# If system install needed:
pip install --user package_name
```

#### 5. Virtual Environment Issues

```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv  # Mac/Linux
rmdir /s venv  # Windows

# Create new environment
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

#### 6. Streamlit Won't Start

```bash
# Check if port 8501 is in use
# Windows
netstat -ano | findstr :8501

# Mac/Linux
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

#### 7. API Key Errors

```bash
# Verify .env file exists
ls -la | grep .env  # Mac/Linux
dir | findstr .env  # Windows

# Check .env contents (without revealing keys)
cat .env | head -1  # Mac/Linux
type .env           # Windows

# Ensure no extra spaces
GROQ_API_KEY=key123  # Correct
GROQ_API_KEY = key123  # Wrong (spaces)
```

#### 8. Audio Recording Not Working

**Browser Permissions:**
- Chrome/Edge: Click lock icon → Microphone → Allow
- Firefox: Permissions → Microphone → Allow
- Safari: Preferences → Websites → Microphone → Allow

**Microphone Issues:**
```bash
# Test system microphone
# Windows: Sound Settings → Test Microphone
# Mac: System Preferences → Sound → Input
# Linux: pavucontrol or alsamixer
```

#### 9. Module Import Errors

```bash
# Ensure you're in virtual environment
which python  # Should show venv path

# Reinstall specific package
pip uninstall package_name
pip install package_name

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 10. Windows PowerShell Execution Policy

```powershell
# If activation script won't run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use alternative activation
& .\venv\Scripts\Activate.ps1
```

---

## Getting API Keys

### Groq API Key

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create new API key
5. Copy key (starts with `gsk_`)

### ElevenLabs API Key

1. Visit [https://elevenlabs.io](https://elevenlabs.io)
2. Sign up or log in
3. Go to Profile → API Keys
4. Generate new API key
5. Copy key

---

## Updating the Application

```bash
# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate   # Windows

# Update dependencies
pip install -r requirements.txt --upgrade

# Run application
cd src
streamlit run app.py
```

---

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
# Windows
rmdir /s /q C:\path\to\LLMProject

# Mac/Linux
rm -rf ~/path/to/LLMProject

# Remove FFmpeg (optional)
# Windows
choco uninstall ffmpeg

# Mac
brew uninstall ffmpeg

# Linux
sudo apt remove ffmpeg
```

---

## Additional Resources

- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **Groq Documentation**: [console.groq.com/docs](https://console.groq.com/docs)
- **ElevenLabs Documentation**: [elevenlabs.io/docs](https://elevenlabs.io/docs)
- **FFmpeg Documentation**: [ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)

---

## Support

If you encounter issues not covered here:

1. Check the error logs
2. Search existing issues on GitHub
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

---

**Last Updated**: February 2026
