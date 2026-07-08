import librosa
import numpy as np


def analyze_pauses(audio_path):

    y, sr = librosa.load(audio_path, sr=None)

    intervals = librosa.effects.split(
        y,
        top_db=30
    )

    total_duration = librosa.get_duration(y=y, sr=sr)

    speaking_duration = 0
    pause_duration = 0
    num_pauses = 0

    previous_end = 0

    MIN_PAUSE = 0.30      # Ignore pauses shorter than 300 ms

    for start, end in intervals:

        start_sec = start / sr
        end_sec = end / sr

        speaking_duration += end_sec - start_sec

        pause = start_sec - previous_end

        if pause >= MIN_PAUSE:
            pause_duration += pause
            num_pauses += 1

        previous_end = end_sec

    # Final pause after speech
    last_pause = total_duration - previous_end

    if last_pause >= MIN_PAUSE:
        pause_duration += last_pause
        num_pauses += 1

    pause_ratio = (pause_duration / total_duration) * 100

    return {
        "total_duration": round(total_duration, 2),
        "speaking_duration": float(round(speaking_duration, 2)),
        "pause_duration": float(round(pause_duration, 2)),
        "pause_ratio": float(round(pause_ratio, 2)),
        "num_pauses": num_pauses
    }
    