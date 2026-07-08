import streamlit as st
from utils.audio_visualizer import plot_waveform
from models.whisper_model import transcribe_audio
from models.analysis import evaluate
from utils.pdf_generator import generate_pdf
from utils.storage import save_session, load_history
from utils.audio_metrics import analyze_pauses
import os

os.makedirs("audio/temp", exist_ok=True)
os.makedirs("reports", exist_ok=True)

st.set_page_config(page_title="VBCUA", layout="wide")
st.markdown("""
<style>

.main-title{
    font-size:38px;
    font-weight:bold;
    color:#1f77b4;
}

.subtitle{
    font-size:18px;
    color:gray;
    margin-bottom:20px;
}

.block-container{
    padding-top:2rem;
}

div[data-testid="metric-container"]{
    border:1px solid #2e2e2e;
    padding:18px;
    border-radius:15px;
    background:#111827;
}

div.stButton > button:first-child {
    background-color: #28a745;
    color: white;
    border-radius: 10px;
    border: none;
    height: 3rem;
    font-weight: bold;
}

div.stButton > button:first-child:hover {
    background-color: #218838;
    color: white;
}



</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;'>
🎧 Voice-Based Concept Understanding Analyser (VBCUA)
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:18px; color:gray;'>
Upload an audio file and get AI-based understanding + scoring.
</p>
""", unsafe_allow_html=True)
with st.sidebar:

    st.title("VBCUA")

    st.info(
        """
AI Modules

• Whisper
• Sentence-BERT
• Librosa
• Report Generator
"""
    )

    st.divider()

    st.success("Ready for Analysis")
    
tab1, tab2 = st.tabs(["📊 Current Analysis", "📜 Session History"])

with tab1:
    with st.container(border=True):

     st.subheader("📤 Upload Audio")

     audio_file = st.file_uploader(
        "Choose Audio",
        type=["wav","mp3","ogg"]
     )

     reference_text = st.text_area(
        "Reference Concept",
        "Newton's third law states..."
     )

    # Initialize variables
    transcript = None
    result = None
    pdf_path = "reports/report.pdf"

    if audio_file is not None:

        file_path = f"audio/temp/{audio_file.name}"

        with open(file_path, "wb") as f:
            f.write(audio_file.read())

        st.audio(file_path)

        with st.container(border=True):

         st.subheader("🎵 Audio Waveform")

         fig = plot_waveform(file_path)

         waveform_path="reports/waveform.png"

         fig.savefig(waveform_path)

         st.pyplot(fig)

        if st.button(
    "🚀 Analyze Speech",
    type="primary",
    use_container_width=True
):

            with st.spinner("Processing..."):

                transcript = transcribe_audio(file_path)
                audio_metrics = analyze_pauses(file_path)

                result = evaluate(transcript, reference_text)
                result.update(audio_metrics)

                generate_pdf(
                    transcript=transcript,
                    scores=result,
                    output_path=pdf_path
                )

            st.success("Analysis Complete!")

            save_session({
                "transcript": transcript,
                "scores": result,
                "reference": reference_text
            })

    # Show results ONLY if they exist
    if transcript and result:

       with st.container(border=True):

         st.subheader("📝 Transcript")

         st.write(transcript)

       
       with st.container(border=True):
        st.subheader("📊 Scores")
        c1,c2=st.columns(2)

        with c1:

         st.metric(
           "🧠 Semantic",
            f"{result['semantic_score']:.2f}"
            )

         st.metric(
            "💬 Clarity",
            f"{result['clarity_score']:.2f}"
        )

        with c2:

         st.metric(
            "🗣 Fluency",
            f"{result['fluency_score']:.2f}"
        )

         st.metric(
            "⭐ Final",
            f"{result['final_score']:.2f}"
         )
         st.progress(result["final_score"]/100)
       with st.container(border=True):
        st.subheader("📊 AI Evaluation")
        if result["final_score"]>=85:
          st.success("Excellent Understanding")

        elif result["final_score"]>=70:
            st.info("Good Understanding")

        elif result["final_score"]>=50:
            st.warning("Moderate Understanding")

        else:
            st.error("Needs Improvement")
       with st.container(border=True):
        st.subheader("🗣️ Filler Word Analysis")

        st.metric("Total Fillers", result["filler_count"])

        if result["filler_details"]:
            st.write("Detected filler words:")

            for word, count in result["filler_details"].items():
                st.write(f"• {word} : {count}")

        else:
            st.success("No filler words detected.")
       with st.container(border=True):
        # Pause analysis (always shown)
        st.subheader("⏸️ Speech Pause Analysis")

        st.metric("Speaking Time", f"{result['speaking_duration']} sec")
        st.metric("Pause Time", f"{result['pause_duration']} sec")
        st.metric("Pause Ratio", f"{result['pause_ratio']} %")
        st.metric("Number of Pauses", result["num_pauses"])

        if result["pause_ratio"] < 10:
            st.success("🟢 Excellent fluency. Very few unnecessary pauses.")

        elif result["pause_ratio"] < 20:
            st.info("🟡 Good speaking pace with natural pauses.")

        elif result["pause_ratio"] < 35:
            st.warning("🟠 Several pauses detected. More practice can improve fluency.")

        else:
            st.error("🔴 Frequent pauses detected. Consider practicing smoother speech delivery.")

       st.download_button(
            "📄 Download Report",
            open(pdf_path, "rb"),
            file_name="VBCUA_Report.pdf",
            mime="application/pdf"
        )
        
with tab2:

    st.header("📜 Session History")

    history = load_history()

    if not history:
        st.info("No previous analyses found.")

    else:

        # Show latest session first
        for i, session in enumerate(reversed(history), start=1):

            with st.expander(
                f"📄 Session {len(history)-i+1} | ⭐ {session['scores']['final_score']:.2f}"
            ):

                st.write("### 📝 Transcript")
                st.write(session["transcript"])

                st.write("### 📚 Reference Concept")
                st.write(session.get("reference", "Not Available"))

                st.write("### 📊 Scores")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Semantic",
                        session["scores"]["semantic_score"]
                    )

                    st.metric(
                        "Fluency",
                        session["scores"]["fluency_score"]
                    )

                with col2:
                    st.metric(
                        "Clarity",
                        session["scores"]["clarity_score"]
                    )

                    st.metric(
                        "Final",
                        session["scores"]["final_score"]
                    )

                # Optional fields (new sessions only)
                if "filler_count" in session["scores"]:

                    st.subheader("🗣️ Filler Words")

                    st.metric(
                        "Total Fillers",
                        session["scores"]["filler_count"]
                    )

                    if session["scores"]["filler_details"]:

                        for word, count in session["scores"]["filler_details"].items():
                            st.write(f"• {word}: {count}")

                    else:
                        st.success("No filler words detected.")

                if "pause_ratio" in session["scores"]:

                    st.subheader("⏸️ Pause Analysis")

                    st.metric(
                        "Speaking Time",
                        f"{session['scores']['speaking_duration']} sec"
                    )

                    st.metric(
                        "Pause Time",
                        f"{session['scores']['pause_duration']} sec"
                    )

                    st.metric(
                        "Pause Ratio",
                        f"{session['scores']['pause_ratio']} %"
                    )

                    st.metric(
                        "Number of Pauses",
                        session["scores"]["num_pauses"]
                    )

                st.write("🕒 Timestamp")

                st.caption(session["timestamp"])       