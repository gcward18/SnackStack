"""OpenAI text-to-speech playback helpers."""

from io import BytesIO

import sounddevice as sd
import soundfile as sf
from openai import OpenAI

TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICE = "alloy"


def synthesize_wav(text: str) -> bytes:
    """Generate WAV speech bytes for non-empty text."""
    if not text.strip():
        raise ValueError("Cannot synthesize empty text.")

    response = OpenAI().audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        response_format="wav",
    )
    return response.read()


def play_wav(wav_data: bytes) -> None:
    """Decode WAV bytes and play them through the default output device."""
    if not wav_data:
        raise ValueError("Cannot play empty audio.")

    audio, sample_rate = sf.read(
        BytesIO(wav_data),
        dtype="float32",
        always_2d=False,
    )
    sd.play(audio, sample_rate)
    sd.wait()


def speak(text: str) -> None:
    """Generate and play speech for the supplied text."""
    play_wav(synthesize_wav(text))
