from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(transcript, scores, output_path):
    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("Voice-Based Concept Understanding Report", styles["Title"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Transcript</b>", styles["Heading2"]))
    story.append(Paragraph(transcript, styles["BodyText"]))
    story.append(Paragraph("Waveform", styles["Heading2"]))

    story.append(
    Image(
        "reports/waveform.png",
        width=450,
        height=150
    )
    )

    story.append(Spacer(1,20))

    story.append(Paragraph("<b>Evaluation Scores</b>", styles["Heading2"]))

    story.append(
        Paragraph(f"Semantic Score: {scores['semantic_score']:.2f}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Fluency Score: {scores['fluency_score']:.2f}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Clarity Score: {scores['clarity_score']:.2f}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Final Score: {scores['final_score']:.2f}", styles["BodyText"])
    )

    doc.build(story)

    return output_path