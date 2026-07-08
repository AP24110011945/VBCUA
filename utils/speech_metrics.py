import re

FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "actually",
    "basically",
    "you know",
    "so",
    "well",
    "hmm"
]


def detect_fillers(transcript):
    transcript = transcript.lower()

    filler_counts = {}

    total = 0

    for filler in FILLER_WORDS:
        pattern = r"\b" + re.escape(filler) + r"\b"
        count = len(re.findall(pattern, transcript))

        if count > 0:
            filler_counts[filler] = count
            total += count

    return {
        "total_fillers": total,
        "details": filler_counts
    }