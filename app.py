"""
app.py — Streamlit Application for Document Summarizer
Can be deployed directly to Streamlit Community Cloud (share.streamlit.io).
"""

import os
import sys
import streamlit as st

# Add backend directory to sys.path to import extractor and summarizer
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from extractor import extract_from_pdf, extract_from_image
from summarizer import generate_summary, LENGTH_INSTRUCTIONS

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Document Summarizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS for Premium Design ───────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4f46e5;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
    }
    .point-card {
        background-color: #f1f5f9;
        border-left: 4px solid #6366f1;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 0 8px 8px 0;
    }
    .suggestion-card {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 0 8px 8px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/summary-list.png", width=64)
    st.title("Settings")
    
    # Resolve API Key: Sidebar input > st.secrets > os.environ
    env_api_key = os.environ.get("GEMINI_API_KEY", "")
    try:
        secret_api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_api_key = ""
        
    default_key = env_api_key or secret_api_key
    
    api_key_input = st.text_input(
        "Gemini API Key",
        value=default_key,
        type="password",
        help="Get your key from Google AI Studio (aistudio.google.com)",
    )
    
    api_key = api_key_input.strip() if api_key_input else default_key
    
    summary_length = st.selectbox(
        "Summary Length",
        options=["short", "medium", "long"],
        index=1,
        format_func=lambda x: x.capitalize() + f" ({'Brief' if x=='short' else 'Balanced' if x=='medium' else 'Detailed'})",
    )
    
    st.markdown("---")
    st.markdown(
        "**Supported File Formats:**\n"
        "- PDF Documents (`.pdf`)\n"
        "- Images (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`)"
    )

# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">✨ AI Document Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload PDFs or scanned images to extract text and generate instant structured summaries powered by Gemini 3.6 Flash.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a file to analyze",
    type=["pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff"],
    help="Maximum file size 20MB",
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_size_mb = len(file_bytes) / (1024 * 1024)
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    if file_size_mb > 20:
        st.error(f"❌ File size ({file_size_mb:.1f}MB) exceeds 20MB limit.")
        st.stop()
        
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"📁 **File:** `{uploaded_file.name}` ({file_size_mb:.2f} MB)")
    with col2:
        process_btn = st.button("🚀 Summarize Document", type="primary", use_container_width=True)
        
    if process_btn:
        if not api_key:
            st.error("⚠️ Gemini API Key is missing. Please enter your API key in the sidebar or configure GEMINI_API_KEY.")
            st.stop()
            
        # 1. Extract Text
        with st.spinner("🔍 Extracting text from document..."):
            try:
                if file_ext == "pdf":
                    extracted_text = extract_from_pdf(file_bytes)
                    doc_type = "PDF"
                else:
                    extracted_text = extract_from_image(file_bytes)
                    doc_type = "Image (OCR)"
            except Exception as e:
                st.error(f"❌ Text extraction failed: {e}")
                st.stop()
                
        if not extracted_text or len(extracted_text.strip()) < 30:
            st.warning("⚠️ Could not extract sufficient text from this document. It may be empty, password-protected, or corrupted.")
            st.stop()
            
        # 2. Generate Summary
        with st.spinner("🤖 Generating AI summary with Gemini 3.6 Flash..."):
            try:
                res = generate_summary(extracted_text, summary_length, api_key)
            except Exception as e:
                st.error(f"❌ Summary generation failed: {e}")
                st.stop()
                
        word_count = len(extracted_text.split())
        char_count = len(extracted_text)
        est_read_time = max(1, round(word_count / 200))
        
        st.success("🎉 Processing complete!")
        st.markdown("---")
        
        # ── Metrics Row ──
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Document Type", doc_type)
        with m2:
            st.metric("Word Count", f"{word_count:,}")
        with m3:
            st.metric("Character Count", f"{char_count:,}")
        with m4:
            st.metric("Est. Read Time", f"~{est_read_time} min")
            
        st.markdown("### Executive Summary")
        st.write(res["summary"])
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 📌 Key Points")
            for pt in res["key_points"]:
                st.markdown(f'<div class="point-card">• {pt}</div>', unsafe_allow_html=True)
                
        with col_right:
            st.markdown("### 💡 Suggestions for Improvement")
            for sug in res["improvement_suggestions"]:
                st.markdown(f'<div class="suggestion-card">💡 {sug}</div>', unsafe_allow_html=True)
                
        # ── Export / Download Option ──
        download_content = f"""# Summary of {uploaded_file.name}

## Executive Summary
{res['summary']}

## Key Points
""" + "\n".join([f"- {pt}" for pt in res["key_points"]]) + "\n\n## Improvement Suggestions\n" + "\n".join([f"- {sug}" for sug in res["improvement_suggestions"]])

        st.markdown("---")
        st.download_button(
            label="📥 Download Summary (.txt)",
            data=download_content,
            file_name=f"{uploaded_file.name}_summary.txt",
            mime="text/plain",
        )
