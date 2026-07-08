from models.semantic_model import evaluate_understanding

reference = "Binary search works on sorted arrays by repeatedly dividing the search space."

student = "Binary search only works on sorted arrays and keeps checking the middle element."

result = evaluate_understanding(reference, student)

print("Semantic Score:", result)