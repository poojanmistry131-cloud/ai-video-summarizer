import streamlit as st
import requests
import os
import base64

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Video Summarizer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; }
p, li, span, div, label { color: #e2e8f0 !important; }
h1, h2, h3 { color: #a78bfa !important; }
.stTextInput input {
    background: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border: 1px solid rgba(167,139,250,0.4) !important;
    border-radius: 10px !important;
}
.stTextInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="base-input"] { background: #ffffff !important; }
.stTextInput input::placeholder { color: #6b7280 !important; -webkit-text-fill-color: #6b7280 !important; }
.stTextInput label { color: #c4b5fd !important; font-weight: 500 !important; }
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 600 !important;
    width: 100% !important;
}
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label { color: #94a3b8 !important; }
[data-testid="metric-container"] [data-testid="metric-value"] { color: #a78bfa !important; font-size: 1.8rem !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.04) !important; border-radius: 10px !important; padding: 4px !important; }
.stTabs [data-baseweb="tab"] { color: #94a3b8 !important; font-weight: 500 !important; border-radius: 8px !important; }
.stTabs [aria-selected="true"] { background: rgba(124,58,237,0.4) !important; color: #ffffff !important; }
.summary-box { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 1.5rem; color: #e2e8f0; line-height: 1.8; }
.quiz-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 1.5rem; margin-bottom: 1.2rem; }
.quiz-question { color: #f1f5f9 !important; font-size: 1rem; font-weight: 600; margin-bottom: 1rem; }
.option-correct { background: rgba(52,211,153,0.15) !important; border: 1px solid rgba(52,211,153,0.4) !important; color: #34d399 !important; border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 0.4rem; }
.option-wrong { background: rgba(248,113,113,0.15) !important; border: 1px solid rgba(248,113,113,0.4) !important; color: #f87171 !important; border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 0.4rem; }
.option-reveal { background: rgba(52,211,153,0.1) !important; border: 1px solid rgba(52,211,153,0.3) !important; color: #6ee7b7 !important; border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 0.4rem; }
.explanation-box { background: rgba(96,165,250,0.1); border: 1px solid rgba(96,165,250,0.25); border-radius: 8px; padding: 0.7rem 1rem; color: #93c5fd !important; font-size: 0.88rem; margin-top: 0.8rem; }
.stTextArea textarea { background: rgba(255,255,255,0.06) !important; color:#000000 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
.score-badge { background: rgba(167,139,250,0.15); border: 1px solid rgba(167,139,250,0.3); border-radius: 50px; padding: 0.4rem 1.2rem; color: #c4b5fd !important; font-weight: 600; display: inline-block; margin-bottom: 1rem; }
.download-link { display: inline-block; background: linear-gradient(135deg, #059669, #10b981); color: white !important; text-decoration: none; padding: 0.55rem 1.4rem; border-radius: 8px; font-weight: 600; font-size: 0.9rem; margin-top: 0.8rem; }
.stDownloadButton > button,
[data-testid="stDownloadButton"] button {
    background: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #000000 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button *,
[data-testid="stDownloadButton"] button * { color: #ffffff !important; }
.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] button:hover {
    background: #1f1f1f !important;
    border-color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)

def check_backend():
    try:
        return requests.get(f"{BACKEND_URL}/", timeout=3).status_code == 200
    except:
        return False

def word_count(text):
    return len(text.split())

if "results" not in st.session_state:
    st.session_state.results = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = {}

st.markdown("<h1 style='text-align:center;font-size:2.5rem;'>🎬 AI Video Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#94a3b8;font-size:1rem;margin-bottom:2rem;'>Paste any YouTube or MP4 URL · Get summary + quiz · Download PDF</p>", unsafe_allow_html=True)

if not check_backend():
    st.error("⚠️ Backend not running! Open terminal → cd backend → uvicorn app.main:app --reload --port 8000")

st.markdown("---")

url = st.text_input("🔗 Video URL", placeholder="https://www.youtube.com/watch?v=...")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    process_btn = st.button("🚀 Analyze Video", use_container_width=True)

if process_btn:
    if not url.strip():
        st.error("❌ Please enter a valid video URL.")
    else:
        st.session_state.results = None
        st.session_state.quiz_submitted = {}
        with st.spinner("⏳ Processing video... Please wait a few minutes..."):
            try:
                response = requests.post(f"{BACKEND_URL}/process", json={"url": url}, timeout=600)
                if response.status_code == 200:
                    st.session_state.results = response.json()
                    st.success("✅ Video processed successfully!")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.Timeout:
                st.error("⏱️ Timeout! Try a shorter video (under 30 min).")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if st.session_state.results:
    data       = st.session_state.results
    transcript = data.get("transcript", "")
    summary    = data.get("summary", "")
    quiz       = data.get("quiz", [])
    pdf_path   = data.get("pdf_path", "")

    wc = word_count(transcript)
    sw = word_count(summary)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📝 Transcript Words", f"{wc:,}")
    c2.metric("📋 Summary Words",    f"{sw:,}")
    c3.metric("🧠 Quiz Questions",   len(quiz))
    c4.metric("📊 Compression",      f"{round(sw/wc*100) if wc>0 else 0}%")

    st.markdown("<br>", unsafe_allow_html=True)
    SECTIONS = ["📋 Summary", "🧠 Quiz", "📝 Transcript", "📄 PDF"]
    if "section" not in st.session_state:
        st.session_state.section = SECTIONS[0]
    section = st.radio(
        "Section",
        SECTIONS,
        horizontal=True,
        key="section",
        label_visibility="collapsed",
    )

    # ── SUMMARY TAB ──────────────────────────────────────────────────────────
    if section == "📋 Summary":
        st.markdown("## 📋 Video Summary")
        st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

    # ── QUIZ TAB ─────────────────────────────────────────────────────────────
    if section == "🧠 Quiz":
        st.markdown("## 🧠 Comprehension Quiz")
        st.markdown("<p style='color:#94a3b8;'>Select your answer then click Submit Answer.</p>", unsafe_allow_html=True)

        total   = len(quiz)
        correct = 0

        for i, item in enumerate(quiz):
            question    = item.get("question", "")
            options     = item.get("options", {})
            right_ans   = item.get("answer", "")
            explanation = item.get("explanation", "")
            s_key       = f"submitted_{i}"
            r_key       = f"radio_{i}"

            st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="quiz-question">Q{i+1}. {question}</div>', unsafe_allow_html=True)

            option_labels = [f"{k}. {v}" for k, v in options.items()]
            selected = st.radio(f"Answer {i+1}", option_labels, key=r_key, label_visibility="collapsed")

            if not st.session_state.quiz_submitted.get(s_key, False):
                if st.button(f"✅ Submit Answer", key=f"sub_{i}"):
                    st.session_state.quiz_submitted[s_key] = selected
                    st.rerun()
            else:
                saved_answer = st.session_state.quiz_submitted[s_key]
                user_key = saved_answer[0] if saved_answer else ""
                if user_key == right_ans:
                    correct += 1
                    st.markdown(f'<div class="option-correct">✅ Correct! You selected: {saved_answer}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="option-wrong">❌ Wrong! You selected: {saved_answer}</div>', unsafe_allow_html=True)
                    correct_text = options.get(right_ans, "")
                    st.markdown(f'<div class="option-reveal">✅ Right Answer: {right_ans}. {correct_text}</div>', unsafe_allow_html=True)
                if explanation:
                    st.markdown(f'<div class="explanation-box">💡 {explanation}</div>', unsafe_allow_html=True)

            st.markdown('</div><br>', unsafe_allow_html=True)

        answered = len(st.session_state.quiz_submitted)
        if answered == total and total > 0:
            pct = round(correct / total * 100)
            emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"
            st.markdown(f'<div class="score-badge">{emoji} Final Score: {correct}/{total} ({pct}%)</div>', unsafe_allow_html=True)
            if st.button("🔄 Retake Quiz"):
                st.session_state.quiz_submitted = {}
                st.rerun()

    # ── TRANSCRIPT TAB ────────────────────────────────────────────────────────
    if section == "📝 Transcript":
        st.markdown("## 📝 Full Transcript")
        st.markdown(f'<div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:10px;padding:1.2rem;color:#f1f5f9;font-size:0.88rem;line-height:1.7;height:400px;overflow-y:scroll;white-space:pre-wrap;">{transcript}</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Transcript (.txt)",
            data=transcript.encode("utf-8"),
            file_name="transcript.txt",
            mime="text/plain",
            key="dl_transcript"
        )

    # ── PDF TAB ───────────────────────────────────────────────────────────────
    if section == "📄 PDF":
        st.markdown("## 📄 PDF Report")
        st.markdown("Download your full summary + quiz as a PDF file.")
        st.markdown("<br>", unsafe_allow_html=True)
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name="summary_quiz.pdf",
                mime="application/pdf",
                key="dl_pdf"
            )
            st.success("✅ PDF ready!")
        else:
            st.warning("⚠️ PDF not found. Process a video first.")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#475569;font-size:0.75rem;'>Powered by Whisper · Groq LLaMA3 · FastAPI · Streamlit</p>", unsafe_allow_html=True)