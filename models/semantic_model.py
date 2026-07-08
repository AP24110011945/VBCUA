from sentence_transformers import SentenceTransformer, util

# Load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(reference_text, student_text):
    """
    Returns similarity score between 0 and 1
    """

    embeddings = model.encode([reference_text, student_text], convert_to_tensor=True)

    score = util.cos_sim(embeddings[0], embeddings[1]).item()

    return round(score, 4)


def evaluate_understanding(reference_text, student_text):
    score = semantic_score(reference_text, student_text)

    return {
        "semantic_score": score,
        "semantic_percentage": round(score * 100, 2)
    }