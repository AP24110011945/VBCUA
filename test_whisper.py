from models.whisper_model import transcribe_audio

print("2. Imported whisper_model")

audio_path = "audio/temp/sample sound.ogg"

print("3. Starting transcription...")

text = transcribe_audio(audio_path)

print("4. Transcription complete!")

print("\nTranscript:")
print(text)