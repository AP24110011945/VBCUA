from models.whisper_model import transcribe_audio
from models.analysis import evaluate

audio_path = "audio/temp/sample sound.ogg"

reference_text = """
Newton's third law states that for every action there is an equal and opposite reaction.
"""

print("1. Transcribing audio...")
transcript = transcribe_audio(audio_path)

print("\n2. Running analysis...")
result = evaluate(transcript, reference_text)

print("\n=== TRANSCRIPT ===")
print(transcript)

print("\n=== SCORES ===")
print(result)