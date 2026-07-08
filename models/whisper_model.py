import whisper

# Load the Whisper model only once
model = whisper.load_model("base")


def transcribe_audio(audio_path):
    """
    Converts speech in an audio file to text.

    Parameters:
        audio_path (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    result = model.transcribe(audio_path)
    return result["text"]