import streamlit as st
import os
from dotenv import load_dotenv
from cartesia import Cartesia
import tempfile
import base64
import time
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TTS Comparison Arena",
    page_icon="🔊",
    layout="wide"
)

# Predefined voices with descriptions
CARTESIA_VOICES = {
    "Barbershop Man": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "Salesman": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
    "Newsman": "79a125e8-cd45-4c13-8a67-188112f4dd22",
    "British Lady": "71a7ad14-091c-4e8e-a314-022ece01c121",
    "Professional Woman": "156fb8d2-335b-4950-9cb3-a2d33befec77",
    "Friendly Woman": "2ee87190-8f84-4925-97da-e52547f9462c",
    "Calm Woman": "694f9389-aac1-45b6-b726-9d9369183238",
    "Storyteller Lady": "a3520a8f-226a-428d-9fcd-b0a4711a6829",
}

CARTESIA_MODELS = {
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


def _load_initial_api_key(key_name: str) -> str:
    """Load an API key from Streamlit secrets or environment without crashing on missing keys."""
    secret_val = None
    try:
        if key_name in st.secrets:
            secret_val = st.secrets[key_name]
    except Exception:
        # st.secrets may not be available locally; ignore
        secret_val = None
    env_val = os.getenv(key_name)
    return (secret_val or env_val or "").strip()


def bootstrap_api_keys():
    """Seed session state with any stored keys so we can use or override them at runtime."""
    if "cartesia_api_key" not in st.session_state:
        st.session_state["cartesia_api_key"] = _load_initial_api_key("CARTESIA_API_KEY")
    if "elevenlabs_api_key" not in st.session_state:
        st.session_state["elevenlabs_api_key"] = _load_initial_api_key("ELEVENLABS_API_KEY")


def render_api_key_controls():
    """Sidebar controls to view status and override API keys for this session."""
    st.subheader("API Keys")
    st.caption("Uses saved env/secrets by default. Provide your own keys to override for this session.")

    cartesia_present = bool(st.session_state.get("cartesia_api_key"))
    eleven_present = bool(st.session_state.get("elevenlabs_api_key"))

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Cartesia key loaded", value=cartesia_present, disabled=True)
    with col2:
        st.checkbox("ElevenLabs key loaded", value=eleven_present, disabled=True)

    cartesia_input = st.text_input(
        "Cartesia API Key",
        value="",
        type="password",
        placeholder="Enter Cartesia API key",
        key="cartesia_key_input",
        help="Overrides any saved key for this session"
    )
    eleven_input = st.text_input(
        "ElevenLabs API Key",
        value="",
        type="password",
        placeholder="Enter ElevenLabs API key",
        key="elevenlabs_key_input",
        help="Overrides any saved key for this session"
    )

    if st.button("Use these keys for this session", use_container_width=True):
        if cartesia_input.strip():
            st.session_state["cartesia_api_key"] = cartesia_input.strip()
        if eleven_input.strip():
            st.session_state["elevenlabs_api_key"] = eleven_input.strip()
        st.success("API keys updated for this session. Keys are not stored on disk.")
        st.rerun()


# ElevenLabs voice options (common voices)
ELEVENLABS_VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Clyde": "2EiwWnXFnvU5JabPnv8n",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Dave": "CYw3kZ02Hs0563khs1Fj",
    "Fin": "D38z5RcWu1voky8WS1ja",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Thomas": "GBv7mTt0atIp3BR8iCZE",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "Emily": "LcfcDJNUP1GQjkzn1xUU",
    "Elli": "MF3mGyEYCl7XYWbV9V6O",
    "Callum": "N2lVS1w4EtoT3dr4eOWO",
    "Patrick": "ODq5zmih8GrVes37Dizd",
    "Harry": "SOYHLrjzK2X1ezoPC6cr",
    "Liam": "TX3LPaxmHKxFdv7VOQHJ",
    "Dorothy": "ThT5KcBeYPX3keUQqHPh",
    "Josh": "TxGEqnHWrfWFTfGW9XjX",
    "Arnold": "VR6AewLTigWG4xSOukaG",
    "Charlotte": "XB0fDUnXU5powFXDhCwa",
    "Alice": "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "James": "ZQe5CZNOzWyzPSCn5a3c",
    "Joseph": "Zlb1dXrM653N07WRdFW3",
    "Jeremy": "bVMeCyTHy58xNoL34h3p",
    "Michael": "flq6f7yk4E4fJM5XTYuZ",
    "Ethan": "g5CIjZEefAph4nQFvHAz",
    "Gigi": "jBpfuIE2acCO8z3wKNLl",
    "Freya": "jsCqWAovK2LkecY7zXl4",
    "Grace": "oWAxZDx7w5VEj9dCyTzz",
    "Daniel": "onwK4e9ZLuTAKqWW03F9",
    "Lily": "pFZP5JQG7iQjIQuC4Bku",
    "Serena": "pMsXgVXv3BLzUgSXRplE",
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Nicole": "piTKgcLEGmPE4e6mEKli",
    "Bill": "pqHfZKP75CvOlQylNhV4",
    "Jessie": "t0jbNlBVZ17f02VDIeMI",
    "Sam": "yoZ06aMxZJJ28mfd3POQ",
    "Glinda": "z9fAnlkpzviPz146aGWa",
    "Giovanni": "zcAOhNBS3c14rBihAFp1",
    "Mimi": "zrHiDhphv9ZnVXBqCLjz",
}


def initialize_cartesia_client():
    """Initialize Cartesia client with API key from environment."""
    api_key = st.session_state.get("cartesia_api_key") or _load_initial_api_key("CARTESIA_API_KEY")
    if not api_key:
        return None
    return Cartesia(api_key=api_key)


def initialize_elevenlabs_client():
    """Initialize ElevenLabs client with API key from environment."""
    api_key = st.session_state.get("elevenlabs_api_key") or _load_initial_api_key("ELEVENLABS_API_KEY")
    if not api_key:
        return None
    return ElevenLabs(api_key=api_key)


def generate_cartesia_speech(client, text, voice_id, model_id, sample_rate):
    """
    Generate speech from text using Cartesia API.

    Args:
        client: Cartesia client instance
        text: Text to convert to speech
        voice_id: Voice ID to use
        model_id: Model ID to use
        sample_rate: Audio sample rate

    Returns:
        tuple: (audio_data in bytes, generation_time in seconds)
    """
    try:
        start_time = time.time()
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
                "container": "mp3",
                "sample_rate": sample_rate
            },
            language="en"
        )

        # Collect all audio chunks
        for chunk in bytes_iter:
            audio_data += chunk

        end_time = time.time()
        generation_time = end_time - start_time

        return audio_data, generation_time

    except Exception as e:
        st.error(f"Error generating Cartesia speech: {str(e)}")
        return None, None


def generate_elevenlabs_speech(client, text, voice_id):
    """
    Generate speech from text using ElevenLabs API.

    Args:
        client: ElevenLabs client instance
        text: Text to convert to speech
        voice_id: Voice ID to use

    Returns:
        tuple: (audio_data in bytes, generation_time in seconds)
    """
    try:
        start_time = time.time()

        # Call the ElevenLabs Text-to-Speech API (current client API)
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
        )

        # Collect all audio chunks (convert returns an iterator of bytes)
        audio_data = b"".join(audio_stream)

        end_time = time.time()
        generation_time = end_time - start_time

        return audio_data, generation_time

    except AttributeError:
        st.error(
            "ElevenLabs client is missing `text_to_speech.convert`. "
            "Upgrade the `elevenlabs` package (e.g., `pip install -U elevenlabs>=1.0.0`)."
        )
        return None, None
    except Exception as e:
        st.error(f"Error generating ElevenLabs speech: {str(e)}")
        return None, None


def render_cartesia_tab():
    """Render the original Cartesia TTS tab."""
    st.markdown("### Cartesia Text-to-Speech")
    st.markdown("Convert text to natural-sounding speech using Cartesia AI's TTS API")

    # Initialize client
    client = initialize_cartesia_client()

    if not client:
        st.error("⚠️ CARTESIA_API_KEY not found in environment variables!")
        st.info("Please create a .env file with your API key or set it as an environment variable.")
        return

    # Sidebar for configuration
    with st.sidebar:
        st.header("🎙️ Cartesia TTS Settings")
# ⚙️
        # Voice selection
        selected_voice_name = st.selectbox(
            "Voice",
            options=list(CARTESIA_VOICES.keys()),
            index=1,
            key="cartesia_voice"
        )
        voice_id = CARTESIA_VOICES[selected_voice_name]

        # Model selection
        selected_model_name = st.selectbox(
            "Model",
            options=list(CARTESIA_MODELS.keys()),
            index=0,
            key="cartesia_model"
        )
        model_id = CARTESIA_MODELS[selected_model_name]

        # Sample rate selection
        selected_sample_rate_name = st.selectbox(
            "Sample Rate",
            options=list(SAMPLE_RATES.keys()),
            index=0,
            key="cartesia_sample_rate"
        )
        sample_rate = SAMPLE_RATES[selected_sample_rate_name]

    # Main content area
    st.markdown("### Enter your text")

    # Text input with default example
    default_text = "To be or not to be. That is the question."

    text_input = st.text_area(
        "Text to convert to speech",
        value=default_text,
        height=150,
        max_chars=5000,
        help="Enter the text you want to convert to speech (max 5000 characters)",
        key="cartesia_text"
    )

    # Character count
    char_count = len(text_input)
    st.caption(f"Characters: {char_count}/5000")

    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("🎙️ Generate Speech", use_container_width=True, type="primary", key="cartesia_generate")

    # Generate and play audio
    if generate_button:
        if not text_input.strip():
            st.warning("Please enter some text to convert to speech.")
        else:
            with st.spinner("Generating speech..."):
                audio_data, gen_time = generate_cartesia_speech(
                    client=client,
                    text=text_input,
                    voice_id=voice_id,
                    model_id=model_id,
                    sample_rate=sample_rate
                )

                if audio_data:
                    st.success(f"✅ Speech generated successfully in {gen_time:.2f} seconds!")

                    # Display audio player
                    st.audio(audio_data, format="audio/mpeg")

                    # Download button
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_data,
                        file_name="cartesia_tts_output.mp3",
                        mime="audio/mpeg"
                    )


def render_comparison_tab():
    """Render the comparison tab for Cartesia vs ElevenLabs."""
    st.markdown("### 🥊 TTS Arena: Cartesia vs ElevenLabs")
    st.markdown("Compare voice outputs from Cartesia and ElevenLabs side-by-side")

    # Ensure session storage for generated samples
    if "comp_results" not in st.session_state:
        st.session_state["comp_results"] = {
            "cartesia_audio": None,
            "cartesia_time": None,
            "eleven_audio": None,
            "eleven_time": None,
        }

    # Initialize clients
    cartesia_client = initialize_cartesia_client()
    elevenlabs_client = initialize_elevenlabs_client()

    # Check API keys
    col1, col2 = st.columns(2)
    with col1:
        if cartesia_client:
            st.success("✅ Cartesia API key loaded")
        else:
            st.error("⚠️ Cartesia API key missing")

    with col2:
        if elevenlabs_client:
            st.success("✅ ElevenLabs API key loaded")
        else:
            st.error("⚠️ ElevenLabs API key missing")

    if not cartesia_client or not elevenlabs_client:
        st.info("Please set both CARTESIA_API_KEY and ELEVENLABS_API_KEY in your .env file to use the comparison feature.")
        return

    

    # Settings in sidebar
    with st.sidebar:
        st.divider()

        st.header("🥊 Comparison Arena Settings")

        st.subheader("Cartesia")
        cartesia_voice_name = st.selectbox(
            "Cartesia Voice",
            options=list(CARTESIA_VOICES.keys()),
            index=1,
            key="comp_cartesia_voice"
        )
        cartesia_voice_id = CARTESIA_VOICES[cartesia_voice_name]

        cartesia_model_name = st.selectbox(
            "Cartesia Model",
            options=list(CARTESIA_MODELS.keys()),
            index=0,
            key="comp_cartesia_model"
        )
        cartesia_model_id = CARTESIA_MODELS[cartesia_model_name]

        st.subheader("ElevenLabs")
        elevenlabs_voice_name = st.selectbox(
            "ElevenLabs Voice",
            options=list(ELEVENLABS_VOICES.keys()),
            index=0,
            key="comp_elevenlabs_voice"
        )
        elevenlabs_voice_id = ELEVENLABS_VOICES[elevenlabs_voice_name]

    # Main content
    st.markdown("### Enter text to compare")

    comparison_text = st.text_area(
        "Text for comparison",
        # value="The quick brown fox jumps over the lazy dog. This is a test of text to speech quality.",
        value="The budget increased from $1,234 to $12,340.50 between 2015 and 2025.",
        height=120,
        max_chars=5000,
        help="Enter the text you want both services to speak (max 5000 characters)",
        key="comparison_text"
    )

    char_count = len(comparison_text)
    st.caption(f"Characters: {char_count}/5000")

    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        compare_button = st.button("⚡ Generate Both", use_container_width=True, type="primary", key="compare_generate")

    # Generate both audio samples
    if compare_button:
        if not comparison_text.strip():
            st.warning("Please enter some text to compare.")
        else:
            # Generate Cartesia audio
            with st.spinner("Generating Cartesia..."):
                cartesia_audio, cartesia_time = generate_cartesia_speech(
                    client=cartesia_client,
                    text=comparison_text,
                    voice_id=cartesia_voice_id,
                    model_id=cartesia_model_id,
                    sample_rate=44100
                )

            if cartesia_audio:
                st.session_state["comp_results"]["cartesia_audio"] = cartesia_audio
                st.session_state["comp_results"]["cartesia_time"] = cartesia_time

            # Generate ElevenLabs audio
            with st.spinner("Generating ElevenLabs..."):
                elevenlabs_audio, elevenlabs_time = generate_elevenlabs_speech(
                    client=elevenlabs_client,
                    text=comparison_text,
                    voice_id=elevenlabs_voice_id
                )

            if elevenlabs_audio:
                st.session_state["comp_results"]["eleven_audio"] = elevenlabs_audio
                st.session_state["comp_results"]["eleven_time"] = elevenlabs_time

    # Always render available audio from session (persists after reruns/downloads)
    if st.session_state["comp_results"]["cartesia_audio"] or st.session_state["comp_results"]["eleven_audio"]:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### 🔵 Cartesia")
            if st.session_state["comp_results"]["cartesia_audio"]:
                st.metric(
                    "Generation Time (Cartesia)",
                    f"{st.session_state['comp_results']['cartesia_time']:.3f}s",
                    help="Measured wall-clock seconds from request start until all audio bytes are received."
                )
                st.audio(st.session_state["comp_results"]["cartesia_audio"], format="audio/mpeg")
                st.download_button(
                    label="📥 Download Cartesia",
                    data=st.session_state["comp_results"]["cartesia_audio"],
                    file_name="cartesia_output.mp3",
                    mime="audio/mpeg",
                    key="download_a"
                )

        with col_b:
            st.markdown("#### 🟢 ElevenLabs")
            if st.session_state["comp_results"]["eleven_audio"]:
                st.metric(
                    "Generation Time (ElevenLabs)",
                    f"{st.session_state['comp_results']['eleven_time']:.3f}s",
                    help="Measured wall-clock seconds from request start until all audio bytes are received."
                )
                st.audio(st.session_state["comp_results"]["eleven_audio"], format="audio/mpeg")
                st.download_button(
                    label="📥 Download ElevenLabs",
                    data=st.session_state["comp_results"]["eleven_audio"],
                    file_name="elevenlabs_output.mp3",
                    mime="audio/mpeg",
                    key="download_b"
                )

            # Voting section
            if st.session_state["comp_results"]["cartesia_audio"] and st.session_state["comp_results"]["eleven_audio"]:
                st.divider()
                st.markdown("### 🗳️ Which one sounds better?")

                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

                with col1:
                    if st.button("👍 Cartesia", use_container_width=True, key="vote_a"):
                        st.session_state['last_vote'] = 'Cartesia'
                        st.success("You preferred Cartesia!")

                with col2:
                    if st.button("👍 ElevenLabs", use_container_width=True, key="vote_b"):
                        st.session_state['last_vote'] = 'ElevenLabs'
                        st.success("You preferred ElevenLabs!")

                with col3:
                    if st.button("🤝 Tie", use_container_width=True, key="vote_tie"):
                        st.session_state['last_vote'] = 'Tie'
                        st.info("You rated them equally!")

                with col4:
                    if st.button("👎 Both Bad", use_container_width=True, key="vote_both_bad"):
                        st.session_state['last_vote'] = 'Both Bad'
                        st.warning("Both need improvement!")

                # Display last vote
                if 'last_vote' in st.session_state:
                    st.caption(f"Last vote: {st.session_state['last_vote']}")


def main():
    bootstrap_api_keys()
    st.title("🔊 TTS Comparison Arena")
    st.warning(
        "This demo is currently configured with personal API tokens from the environment. "
        "Please enter your own Cartesia and ElevenLabs API keys in the sidebar before continued use."
    )

    # Global sidebar controls for API keys
    with st.sidebar:
        render_api_key_controls()
        st.divider()

    # Create tabs
    tab1, tab2 = st.tabs(["🎙️ Cartesia TTS", "🥊 Comparison Arena"])

    with tab1:
        render_cartesia_tab()

    with tab2:
        render_comparison_tab()

    # Footer
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Powered by <a href='https://cartesia.ai' target='_blank'>Cartesia AI</a> "
        "and <a href='https://elevenlabs.io' target='_blank'>ElevenLabs</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
