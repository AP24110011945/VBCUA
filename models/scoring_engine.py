import re
import numpy as np

def calculate_fluency(transcript, duration_seconds=None):
    """
    Basic fluency estimation:
    - word rate
    - filler words penalty
    """

    words = transcript.split()
    word_count = len(words)

    # Estimate speaking rate
    if duration_seconds:
        wpm = (word_count / duration_seconds) * 60
    else:
        wpm = word_count  # fallback

    # filler words detection
    fillers = ["um", "uh", "like", "you know", "actually"]
    filler_count = sum(transcript.lower().count(f) for f in fillers)

    filler_penalty = min(filler_count * 2, 30)

    # normalize fluency score
    base = 100 - filler_penalty

    if wpm < 80:
        base -= 10
    elif wpm > 180:
        base -= 10

    return max(0, min(100, base))


def calculate_clarity(transcript):
    """
    Simple clarity estimation:
    - sentence structure
    - repetition penalty
    """

    sentences = re.split(r'[.!?]', transcript)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0

    avg_len = np.mean([len(s.split()) for s in sentences])

    repetition_penalty = len(set(transcript.split())) / len(transcript.split())

    score = 100

    if avg_len < 5:
        score -= 20
    elif avg_len > 25:
        score -= 10

    score *= repetition_penalty

    return round(max(0, min(100, score)), 2)


def final_score(semantic, fluency, clarity):
    return round((semantic + fluency + clarity) / 3, 2)