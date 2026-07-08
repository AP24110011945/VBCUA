from models.whisper_model import transcribe_audio
from models.analysis import analyze_text
from utils.pdf_generator import generate_pdf

audio_path = "audio/temp/sample sound.ogg"

print("1. Transcribing...")
text = transcribe_audio(audio_path)

print("2. Analyzing...")
result = analyze_text(text)

print("3. Generating PDF...")
pdf_path = "reports/output.pdf"

generate_pdf(
    pdf_path,
    result["clean_text"],
    result["summary"],
    result["keywords"]
)

print("DONE ✔ PDF saved at:", pdf_path)