# Cartesia TTS + ElevenLabs Arena (Streamlit)

A clean Streamlit app to convert text to speech with [Cartesia AI](https://cartesia.ai) and a head-to-head comparison tab against ElevenLabs.

## Features

- 🎙️ **Natural-sounding speech** using Cartesia's Sonic 3 model
- 🎨 **Multiple voices** to choose from (professional, casual, narrative styles)
- ⚙️ **Configurable settings** (model, sample rate, voice selection)
- 🎧 **Instant playback** in the browser
- 📥 **Download audio** as MP3 files
- 🔑 **API key flexibility** — uses env/Streamlit secrets by default, lets you paste keys in the sidebar per session
- 🚀 **Minimal dependencies** - no Docker or Kubernetes required
- 💻 **Cross-platform** - runs on Mac, Linux, and Windows

## Prerequisites

- Python 3.8 or higher
- Cartesia AI API key ([sign up here](https://cartesia.ai))
- ElevenLabs API key (only needed for the comparison tab)

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

Edit `.env` and add your keys:

```
CARTESIA_API_KEY=your_actual_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Features

- 🎙️ **Cartesia TTS tab:** pick a Cartesia voice/model/sample rate, enter up to 5,000 characters, listen inline, and download MP3 output.
- 🥊 **Comparison Arena tab:** side-by-side generation for Cartesia (Model A) and ElevenLabs (Model B) with voice pickers, timing metrics, audio players, downloads, and a quick voting widget.
- 🔑 **API key checks & overrides:** surfaces whether each provider’s key is loaded and lets you paste your own keys in the sidebar; ElevenLabs is optional unless you use the arena.
- 🧾 **Light footprint:** Streamlit, Cartesia SDK, ElevenLabs SDK, python-dotenv.

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

### Cartesia tab
1. Enter text (up to 5,000 characters).
2. Select a Cartesia voice, model (Sonic 3 recommended), and sample rate (44.1 kHz default).
3. Click “Generate Speech” to create audio, listen inline, or download an MP3.

### Comparison Arena tab
1. Ensure both `CARTESIA_API_KEY` and `ELEVENLABS_API_KEY` are set.
2. Enter shared text.
3. Pick voices for Cartesia and ElevenLabs.
4. Click “Generate Both” to hear each, see generation times, download outputs, and cast a quick vote.

### API key handling
- The app loads keys from `.env` or Streamlit secrets by default.
- A warning banner reminds you to bring your own keys; use the sidebar API key section to paste Cartesia and/or ElevenLabs keys for the current session (keys are not stored on disk).

## Project Structure

```
cartesia-exploration-and-assessment/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .env                # Your API key (git-ignored)
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

This project uses minimal dependencies:
- **streamlit** - Web application framework
- **cartesia** - Official Cartesia AI Python SDK
- **python-dotenv** - Environment variable management

## API Documentation

For more information about Cartesia's API:
- [Cartesia API Documentation](https://docs.cartesia.ai/)
- [Python SDK on PyPI](https://pypi.org/project/cartesia/)
- [GitHub Repository](https://github.com/cartesia-ai/cartesia-python)

## License

This project is provided as-is for demonstration purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
