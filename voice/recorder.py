"""Microphone recording and OpenAI Whisper transcription helpers."""

from io import BytesIO

import sounddevice as sd
import soundfile as sf
from openai import OpenAI

DEFAULT_DURATION_SECONDS = 5.0
SAMPLE_RATE = 16_000


def record_wav(
    duration: float = DEFAULT_DURATION_SECONDS,
    sample_rate: int = SAMPLE_RATE,
) -> bytes:
    """Record mono microphone audio and encode it as an in-memory WAV file."""
    if duration <= 0:
        raise ValueError("Recording duration must be greater than zero.")

    frame_count = int(duration * sample_rate)
    audio = sd.rec(
        frame_count,
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
    )
    sd.wait()

    buffer = BytesIO()
    sf.write(buffer, audio, sample_rate, format="WAV", subtype="PCM_16")
    return buffer.getvalue()


def transcribe_wav(wav_data: bytes) -> str:
    """Transcribe WAV bytes with OpenAI Whisper."""
    if not wav_data:
        raise ValueError("Cannot transcribe empty audio.")

    transcript = OpenAI().audio.transcriptions.create(
        model="whisper-1",
        file=("recording.wav", wav_data, "audio/wav"),
    )
    return transcript.text.strip()


def record_and_transcribe(
    duration: float = DEFAULT_DURATION_SECONDS,
) -> str:
    """Record one microphone turn and return its transcription."""
    return transcribe_wav(record_wav(duration=duration))
