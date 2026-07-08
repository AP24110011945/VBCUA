from utils.speech_metrics import detect_fillers

text = """
Um I think machine learning is basically a way
to make computers learn. Like, you know,
they improve from data.
"""

result = detect_fillers(text)

print(result)