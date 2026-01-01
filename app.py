import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- CONFIG ----------------

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Document QA System", layout="wide")
st.title("📄 Document-Based Question Answering System")

# ---------------- SESSION STATE ----------------

if "file_ids" not in st.session_state:
    st.session_state.file_ids = []

if "chat" not in st.session_state:
    st.session_state.chat = []

if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = []

# ---------------- HELPERS ----------------

def upload_file_to_openai(uploaded_file):
    """Upload file to OpenAI while preserving extension."""
    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    file = client.files.create(
        file=open(tmp_path, "rb"),
        purpose="assistants"
    )

    return file.id


def ask_documents(file_ids, question):
    """Ask a question using multiple uploaded documents."""
    content = [{"type": "input_text", "text": question}]

    for fid in file_ids:
        content.append({"type": "input_file", "file_id": fid})

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": content
        }]
    )

    return response.output_text

# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 📊 Session Info")
st.sidebar.write("📄 Documents uploaded:", len(st.session_state.file_ids))
st.sidebar.write("💬 Questions asked:", len(st.session_state.chat))

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat = []

# ---------------- UI ----------------

uploaded_files = st.file_uploader(
    "Upload PDF or Word documents",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Uploading documents..."):
        for file in uploaded_files:
            if file.name not in st.session_state.uploaded_names:
                file_id = upload_file_to_openai(file)
                st.session_state.file_ids.append(file_id)
                st.session_state.uploaded_names.append(file.name)

    st.success("📂 Documents uploaded successfully")

# ---------------- QUESTION INPUT ----------------

question = st.text_input(
    "Ask a question from the uploaded document(s)",
    placeholder="e.g. What is the main conclusion of the document?"
)

if question and st.session_state.file_ids:
    with st.spinner("Generating answer..."):
        answer = ask_documents(st.session_state.file_ids, question)

    st.session_state.chat.append({
        "question": question,
        "answer": answer
    })

# ---------------- CHAT DISPLAY ----------------

for i, msg in enumerate(reversed(st.session_state.chat)):
    st.markdown("**🧑 You:** " + msg["question"])
    st.markdown(
        f"<div style='background:#f0f2f6;padding:15px;border-radius:10px'>"
        f"{msg['answer']}</div>",
        unsafe_allow_html=True
    )

    # ✅ Unique key per download button
    st.download_button(
        label="📥 Download Answer",
        data=msg["answer"],
        file_name=f"answer_{i+1}.txt",
        mime="text/plain",
        key=f"download_{i+1}"
    )

    st.markdown("---")
