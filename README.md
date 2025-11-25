# Cartesia AI Exploration & Assessment

A collection of Streamlit applications for exploring conversational AI and text-to-speech capabilities using Cartesia AI, OpenAI, and Anthropic APIs.

## Applications

### 1. 🎤 AI Voice Conversation (`conversation_app.py`)
A bi-directional streaming conversation app that enables natural voice conversations with AI.

**Features:**
- 🎙️ **Voice input** using browser's audio recorder
- 🎧 **Speech-to-text** using OpenAI Whisper
- 🤖 **Conversational AI** powered by Anthropic Claude
- 🔊 **Voice responses** using Cartesia TTS
- 💬 **Multi-turn conversations** with history tracking
- ⚡ **Real-time processing** without button clicks
- 📊 **Performance metrics** showing response times for each step

### 2. 🔊 Text-to-Speech Demo (`app.py`)
A simple TTS demo for converting text to natural-sounding speech.

**Features:**
- 🎙️ **Natural-sounding speech** using Cartesia's Sonic 3 model
- 🎨 **Multiple voices** to choose from (professional, casual, narrative styles)
- ⚙️ **Configurable settings** (model, sample rate, voice selection)
- 🎧 **Instant playback** in the browser
- 📥 **Download audio** as WAV files
- 🚀 **Minimal dependencies** - no Docker or Kubernetes required
- 💻 **Cross-platform** - runs on Mac, Linux, and Windows

## Prerequisites

- Python 3.8 or higher
- **Cartesia AI API key** ([sign up here](https://cartesia.ai)) - for text-to-speech
- **OpenAI API key** ([sign up here](https://platform.openai.com)) - for speech-to-text (conversation app only)
- **Anthropic API key** ([sign up here](https://console.anthropic.com)) - for AI conversation (conversation app only)

## Local Setup (Mac)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd cartesia-exploration-and-assessment
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

**For the TTS demo (`app.py`):**
```
CARTESIA_API_KEY=your_actual_api_key_here
```

**For the conversation app (`conversation_app.py`), add all three:**
```
CARTESIA_API_KEY=your_cartesia_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 5. Run the applications

**For the AI Voice Conversation app:**
```bash
streamlit run conversation_app.py
```

**For the simple TTS demo:**
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## EC2 Deployment

### 1. Launch an EC2 Instance

- Choose Ubuntu Server 22.04 LTS or Amazon Linux 2023
- Instance type: t2.micro or larger (t2.small recommended)
- Configure Security Group to allow:
  - SSH (port 22) from your IP
  - HTTP (port 80) or custom port (e.g., 8501) from anywhere

### 2. Connect to your EC2 instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 3. Install Python and dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install git if not present
sudo apt install git -y
```

### 4. Clone and setup the application

```bash
# Clone repository
git clone <your-repo-url>
cd cartesia-exploration-and-assessment

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure environment

```bash
# Create .env file
cp .env.example .env
nano .env  # Add your API key
```

### 6. Run with Streamlit

For testing:
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### 7. Run as a background service (Production)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/cartesia-tts.service
```

Add the following content (adjust paths as needed):

```ini
[Unit]
Description=Cartesia TTS Streamlit Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cartesia-exploration-and-assessment
Environment="PATH=/home/ubuntu/cartesia-exploration-and-assessment/venv/bin"
ExecStart=/home/ubuntu/cartesia-exploration-and-assessment/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cartesia-tts
sudo systemctl start cartesia-tts
sudo systemctl status cartesia-tts
```

### 8. Access the application

Visit `http://your-ec2-public-ip:8501` in your browser.

### Optional: Setup Nginx reverse proxy (for port 80)

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/cartesia-tts
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or use EC2 public IP

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/cartesia-tts /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Now access via `http://your-ec2-public-ip`

## Usage

### AI Voice Conversation App (`conversation_app.py`)

1. **Click the microphone icon** in the audio recorder to start recording
2. **Speak your message** clearly into your microphone
3. **Click stop** when you're done speaking
4. The system will **automatically**:
   - Transcribe your speech using OpenAI Whisper
   - Generate an AI response using Claude
   - Convert the response to speech using Cartesia
   - Play the audio response
5. **View the conversation history** in the right panel
6. **Record another message** to continue the conversation
7. **Monitor performance metrics** to assess response speed

**Tips:**
- Speak clearly and avoid background noise for best transcription
- Keep messages conversational for natural responses
- Use the reset button to start a new conversation
- Adjust the system prompt in the sidebar to change AI behavior

### Text-to-Speech Demo (`app.py`)

1. **Enter text** in the text area (up to 5000 characters)
2. **Select a voice** from the sidebar dropdown
3. **Choose a model** (Sonic 3 recommended)
4. **Select sample rate** (44.1 kHz for best quality)
5. **Click "Generate Speech"** to create audio
6. **Listen** using the built-in audio player
7. **Download** the audio file if needed

## Available Voices

The application includes several pre-configured voices:
- Barbershop Man
- Salesman
- Newsman
- British Lady
- Professional Woman
- Friendly Woman
- Calm Woman
- Storyteller Lady

## Project Structure

```
cartesia-exploration-and-assessment/
├── conversation_app.py # AI voice conversation app (STT + LLM + TTS)
├── app.py              # Simple text-to-speech demo
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .env                # Your API keys (git-ignored)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Troubleshooting

### "CARTESIA_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify the API key is correctly set in `.env`
- Try restarting the application

### Audio doesn't play
- Check browser console for errors
- Try a different browser (Chrome/Firefox recommended)
- Verify internet connection
- Check that audio isn't muted

### EC2 instance not accessible
- Verify Security Group allows inbound traffic on port 8501 (or 80)
- Check that the service is running: `sudo systemctl status cartesia-tts`
- Verify firewall settings: `sudo ufw status`

### High latency
- Use a larger EC2 instance type (t2.small or better)
- Choose a region closer to your location
- Check network connectivity

## Dependencies

This project uses the following dependencies:
- **streamlit** - Web application framework
- **cartesia** - Official Cartesia AI Python SDK for text-to-speech
- **openai** - OpenAI API client for Whisper speech-to-text
- **anthropic** - Anthropic API client for Claude conversation
- **python-dotenv** - Environment variable management

## API Documentation

For more information about the APIs used:

**Cartesia AI (Text-to-Speech):**
- [Cartesia API Documentation](https://docs.cartesia.ai/)
- [Python SDK on PyPI](https://pypi.org/project/cartesia/)
- [GitHub Repository](https://github.com/cartesia-ai/cartesia-python)

**OpenAI (Speech-to-Text):**
- [Whisper API Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

**Anthropic (Conversational AI):**
- [Claude API Documentation](https://docs.anthropic.com/)
- [Anthropic API Reference](https://docs.anthropic.com/claude/reference)

## License

This project is provided as-is for demonstration purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
