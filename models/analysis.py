from sentence_transformers import SentenceTransformer, util
from models.scoring_engine import calculate_fluency, calculate_clarity, final_score
from utils.speech_metrics import detect_fillers

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(transcript, reference_text):
    emb1 = model.encode(transcript, convert_to_tensor=True)
    emb2 = model.encode(reference_text, convert_to_tensor=True)

    score = util.pytorch_cos_sim(emb1, emb2).item()

    return round(score, 4)


def evaluate(transcript, reference_text, duration=None):

    semantic = semantic_score(transcript, reference_text) * 100
    fluency = calculate_fluency(transcript, duration)
    clarity = calculate_clarity(transcript)

    final = final_score(semantic, fluency, clarity)
    fillers = detect_fillers(transcript)

    return {
        "filler_count": fillers["total_fillers"],
        "filler_details": fillers["details"],
        "semantic_score": round(semantic, 2),
        "fluency_score": fluency,
        "clarity_score": clarity,
        "final_score": final
    }
    