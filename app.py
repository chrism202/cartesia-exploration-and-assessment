import streamlit as st
import os
from dotenv import load_dotenv
from cartesia import Cartesia
import tempfile
import base64

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cartesia TTS Demo",
    page_icon="🔊",
    layout="centered"
)

# Predefined voices with descriptions
VOICES = {
    "Barbershop Man": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "Salesman": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
    "Newsman": "79a125e8-cd45-4c13-8a67-188112f4dd22",
    "British Lady": "71a7ad14-091c-4e8e-a314-022ece01c121",
    "Professional Woman": "156fb8d2-335b-4950-9cb3-a2d33befec77",
    "Friendly Woman": "2ee87190-8f84-4925-97da-e52547f9462c",
    "Calm Woman": "694f9389-aac1-45b6-b726-9d9369183238",
    "Storyteller Lady": "a3520a8f-226a-428d-9fcd-b0a4711a6829",
}

MODELS = {
    "Sonic 3 (Latest)": "sonic-3",
    "Sonic English": "sonic-english",
    "Sonic Multilingual": "sonic-multilingual",
}

SAMPLE_RATES = {
    "44.1 kHz (CD Quality)": 44100,
    "22.05 kHz": 22050,
    "16 kHz": 16000,
    "8 kHz": 8000,
}


def initialize_client():
    """Initialize Cartesia client with API key from environment."""
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key:
        st.error("⚠️ CARTESIA_API_KEY not found in environment variables!")
        st.info("Please create a .env file with your API key or set it as an environment variable.")
        st.stop()
    return Cartesia(api_key=api_key)


def generate_speech(client, text, voice_id, model_id, sample_rate):
    """
    Generate speech from text using Cartesia API.

    Args:
        client: Cartesia client instance
        text: Text to convert to speech
        voice_id: Voice ID to use
        model_id: Model ID to use
        sample_rate: Audio sample rate

    Returns:
        bytes: Audio data in WAV format
    """
    try:
        audio_data = b""

        # Call the Cartesia TTS API
        bytes_iter = client.tts.bytes(
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

        # Collect all audio chunks
        for chunk in bytes_iter:
            audio_data += chunk

        return audio_data

    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None


def main():
    st.title("🔊 Cartesia Text-to-Speech")
    st.markdown("Convert text to natural-sounding speech using Cartesia AI's TTS API")

    # Initialize client
    client = initialize_client()

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Voice selection
        selected_voice_name = st.selectbox(
            "Voice",
            options=list(VOICES.keys()),
            index=1
        )
        voice_id = VOICES[selected_voice_name]

        # Model selection
        selected_model_name = st.selectbox(
            "Model",
            options=list(MODELS.keys()),
            index=0
        )
        model_id = MODELS[selected_model_name]

        # Sample rate selection
        selected_sample_rate_name = st.selectbox(
            "Sample Rate",
            options=list(SAMPLE_RATES.keys()),
            index=0
        )
        sample_rate = SAMPLE_RATES[selected_sample_rate_name]

        st.divider()
        st.markdown("### About")
        st.markdown("This app uses [Cartesia AI's](https://cartesia.ai) text-to-speech API to generate natural-sounding speech.")

    # Main content area
    st.markdown("### Enter your text")

    # Text input with default example
    default_text = "Hello! This is a demonstration of Cartesia's text to speech technology. It sounds remarkably natural and realistic."

    text_input = st.text_area(
        "Text to convert to speech",
        value=default_text,
        height=150,
        max_chars=5000,
        help="Enter the text you want to convert to speech (max 5000 characters)"
    )

    # Character count
    char_count = len(text_input)
    st.caption(f"Characters: {char_count}/5000")

    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("🎙️ Generate Speech", use_container_width=True, type="primary")

    # Generate and play audio
    if generate_button:
        if not text_input.strip():
            st.warning("Please enter some text to convert to speech.")
        else:
            with st.spinner("Generating speech..."):
                audio_data = generate_speech(
                    client=client,
                    text=text_input,
                    voice_id=voice_id,
                    model_id=model_id,
                    sample_rate=sample_rate
                )

                if audio_data:
                    st.success("✅ Speech generated successfully!")

                    # Display audio player
                    st.audio(audio_data, format="audio/wav")

                    # Download button
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_data,
                        file_name="cartesia_tts_output.wav",
                        mime="audio/wav"
                    )

    # Footer
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Powered by <a href='https://cartesia.ai' target='_blank'>Cartesia AI</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
