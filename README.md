# 📄 Document-Based Question Answering System

This is a **Streamlit app** that allows you to upload PDF or Word documents and ask questions using **OpenAI GPT models**. The app supports multi-document queries, keeps a chat history, and allows you to download answers.

---

## Features

- ✅ Upload multiple PDF or DOCX documents
- ✅ Ask questions from the uploaded documents
- ✅ Chat history per session
- ✅ Download answers as `.txt` files
- ✅ Clear chat functionality
- ✅ Document info sidebar
- ✅ Clean, easy-to-use interface
- ✅ No LangChain needed; uses OpenAI API directly

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it:

*- Windows (PowerShell)*

```bash
.venv\Scripts\Activate.ps1
```

*- macOS / Linux*

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a file called .env in the root directory:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```


### 5. Run the app

```bash
streamlit run app.py
```

- The app will open in your browser (usually at http://localhost:8501).

- Upload your documents, ask questions, and download answers.

## Notes

- This app uses the GPT-4.1-mini or GPT-4o-mini models for answering questions.

- Only .pdf and .docx files are supported.

- Make sure your documents contain text, not just scanned images. Scanned PDFs may not work well without OCR.

- Each question is answered strictly based on the uploaded documents.

## File Structure
Document-Based Question Answering System/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignore .env and cache files                 
└── README.md             # This file
