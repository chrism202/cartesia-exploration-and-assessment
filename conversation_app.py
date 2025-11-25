import streamlit as st
import os
from dotenv import load_dotenv
from cartesia import Cartesia
from openai import OpenAI
from anthropic import Anthropic
import tempfile
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Voice Conversation",
    page_icon="🎤",
    layout="wide"
)

# Predefined voices
VOICES = {
    "Professional Woman": "156fb8d2-335b-4950-9cb3-a2d33befec77",
    "Friendly Woman": "2ee87190-8f84-4925-97da-e52547f9462c",
    "Calm Woman": "694f9389-aac1-45b6-b726-9d9369183238",
    "Barbershop Man": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "Salesman": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
    "Newsman": "79a125e8-cd45-4c13-8a67-188112f4dd22",
}

# Initialize clients
@st.cache_resource
def initialize_clients():
    """Initialize API clients."""
    cartesia_key = os.getenv("CARTESIA_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    errors = []
    if not cartesia_key:
        errors.append("CARTESIA_API_KEY")
    if not openai_key:
        errors.append("OPENAI_API_KEY")
    if not anthropic_key:
        errors.append("ANTHROPIC_API_KEY")

    if errors:
        st.error(f"⚠️ Missing API keys: {', '.join(errors)}")
        st.info("Please add these keys to your .env file")
        st.stop()

    return {
        "cartesia": Cartesia(api_key=cartesia_key),
        "openai": OpenAI(api_key=openai_key),
        "anthropic": Anthropic(api_key=anthropic_key)
    }


def transcribe_audio(audio_bytes, openai_client):
    """
    Transcribe audio using OpenAI Whisper.

    Args:
        audio_bytes: Audio data in bytes
        openai_client: OpenAI client instance

    Returns:
        str: Transcribed text
    """
    try:
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Transcribe using Whisper
        with open(temp_audio_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )

        # Clean up temp file
        os.unlink(temp_audio_path)

        return transcript.text

    except Exception as e:
        st.error(f"Transcription error: {str(e)}")
        return None


def get_ai_response(messages, anthropic_client, model="claude-3-5-sonnet-20241022"):
    """
    Get response from Claude.

    Args:
        messages: List of conversation messages
        anthropic_client: Anthropic client instance
        model: Model to use

    Returns:
        str: AI response text
    """
    try:
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=messages
        )

        return response.content[0].text

    except Exception as e:
        st.error(f"AI response error: {str(e)}")
        return None


def synthesize_speech(text, voice_id, cartesia_client, model_id="sonic-3", sample_rate=44100):
    """
    Generate speech from text using Cartesia.

    Args:
        text: Text to convert to speech
        voice_id: Voice ID to use
        cartesia_client: Cartesia client instance
        model_id: Model ID to use
        sample_rate: Audio sample rate

    Returns:
        bytes: Audio data in WAV format
    """
    try:
        audio_data = b""

        bytes_iter = cartesia_client.tts.bytes(
            model_id=model_id,
            transcript=text,
            voice={
                "mode": "id",
                "id": voice_id
            },
            output_format={
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": sample_rate
            },
            language="en"
        )

        for chunk in bytes_iter:
            audio_data += chunk

        return audio_data

    except Exception as e:
        st.error(f"Speech synthesis error: {str(e)}")
        return None


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None


def main():
    st.title("🎤 AI Voice Conversation")
    st.markdown("Have a natural voice conversation with AI - speak and get spoken responses!")

    # Initialize session state
    initialize_session_state()

    # Initialize clients
    clients = initialize_clients()

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Voice selection
        selected_voice_name = st.selectbox(
            "AI Voice",
            options=list(VOICES.keys()),
            index=0
        )
        voice_id = VOICES[selected_voice_name]

        # Model selection
        ai_model = st.selectbox(
            "AI Model",
            options=[
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229"
            ],
            index=0
        )

        st.divider()

        # System prompt
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful, friendly AI assistant. Keep your responses concise and conversational, as they will be converted to speech. Aim for responses under 3 sentences unless more detail is specifically requested.",
            height=150
        )

        st.divider()

        # Conversation controls
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.session_state.last_audio_hash = None
            st.rerun()

        st.divider()
        st.markdown("### About")
        st.markdown("This app combines:")
        st.markdown("- **OpenAI Whisper** for speech-to-text")
        st.markdown("- **Anthropic Claude** for conversation")
        st.markdown("- **Cartesia AI** for text-to-speech")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎙️ Speak to AI")
        st.markdown("Record your message using the audio recorder below:")

        # Audio input
        audio_input = st.audio_input("Record your message")

        if audio_input is not None:
            # Calculate hash of audio to detect new recordings
            audio_bytes = audio_input.read()
            audio_hash = hash(audio_bytes)

            # Only process if this is a new recording
            if audio_hash != st.session_state.last_audio_hash:
                st.session_state.last_audio_hash = audio_hash
                st.session_state.conversation_started = True

                # Show processing status
                with st.status("Processing your message...", expanded=True) as status:
                    # Step 1: Transcribe
                    st.write("🎧 Transcribing audio...")
                    start_time = time.time()
                    user_text = transcribe_audio(audio_bytes, clients["openai"])
                    transcription_time = time.time() - start_time

                    if user_text:
                        st.write(f"✅ Transcription: \"{user_text}\" ({transcription_time:.2f}s)")

                        # Add user message to conversation
                        st.session_state.messages.append({
                            "role": "user",
                            "content": user_text,
                            "timestamp": datetime.now()
                        })

                        # Step 2: Get AI response
                        st.write("🤖 Getting AI response...")
                        start_time = time.time()

                        # Prepare messages for Claude (with system prompt)
                        claude_messages = []
                        for msg in st.session_state.messages:
                            if msg["role"] in ["user", "assistant"]:
                                claude_messages.append({
                                    "role": msg["role"],
                                    "content": msg["content"]
                                })

                        ai_response = get_ai_response(claude_messages, clients["anthropic"], ai_model)
                        ai_response_time = time.time() - start_time

                        if ai_response:
                            st.write(f"✅ AI Response: \"{ai_response}\" ({ai_response_time:.2f}s)")

                            # Add AI response to conversation
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": ai_response,
                                "timestamp": datetime.now()
                            })

                            # Step 3: Synthesize speech
                            st.write("🔊 Generating speech...")
                            start_time = time.time()
                            audio_data = synthesize_speech(ai_response, voice_id, clients["cartesia"])
                            tts_time = time.time() - start_time

                            if audio_data:
                                st.write(f"✅ Speech generated ({tts_time:.2f}s)")
                                total_time = transcription_time + ai_response_time + tts_time
                                status.update(
                                    label=f"✅ Complete! Total time: {total_time:.2f}s",
                                    state="complete"
                                )

                                # Play the audio
                                st.audio(audio_data, format="audio/wav", autoplay=True)

    with col2:
        st.markdown("### 💬 Conversation History")

        if st.session_state.conversation_started and st.session_state.messages:
            # Display conversation history
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.write(msg["content"])
                        st.caption(msg["timestamp"].strftime("%I:%M:%S %p"))
                else:
                    with st.chat_message("assistant"):
                        st.write(msg["content"])
                        st.caption(msg["timestamp"].strftime("%I:%M:%S %p"))
        else:
            st.info("👆 Start a conversation by recording your first message!")

    # Instructions
    st.divider()
    st.markdown("""
    ### 📖 How to use:
    1. **Click the microphone** icon to start recording
    2. **Speak your message** clearly
    3. **Click stop** when finished
    4. The AI will **automatically**:
       - Transcribe your speech
       - Generate a response
       - Speak the response back to you
    5. **Record again** for the next turn in the conversation

    **Tip:** Keep messages clear and concise for best results!
    """)


if __name__ == "__main__":
    main()
