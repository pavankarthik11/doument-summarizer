# 📄 Doc Summarizer

An AI-powered document analysis web application that extracts text from **PDF files** and **scanned images**, then generates smart summaries with key points and improvement suggestions using **Google Gemini 1.5 Flash**.

## ✨ Features

- 📤 **Drag & drop or file picker** for PDF and image uploads
- 📕 **PDF text extraction** with page-by-page parsing (PyMuPDF)
- 🖼️ **OCR support** for scanned images (Tesseract)
- 🤖 **AI-powered summaries** via Google Gemini 1.5 Flash
- 📏 **Adjustable summary length** — Short, Medium, or Long
- 🎯 **Key points** highlighted automatically
- 💡 **Improvement suggestions** for the document
- 📋 **Copy to clipboard** functionality
- 🌙 **Premium dark glassmorphism UI**, fully responsive

---

## 🏗️ Architecture

```
frontend/ (React + Vite)    →    backend/ (FastAPI + Python)    →    Google Gemini API
```

---

## 🚀 Setup & Running Locally

### Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.9+ | |
| Node.js | 18+ | |
| Tesseract OCR | 5.x | For image OCR support |

### Installing Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default path: `C:\Program Files\Tesseract-OCR\`
3. Add to PATH: `C:\Program Files\Tesseract-OCR\`

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install tesseract-ocr
```

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be available at `http://localhost:5173`

---

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)
5. Paste it into the **API Key** field in the app UI

> **Free tier:** 15 requests/minute, 1 million tokens/day — more than enough for testing.

---

## 📁 Project Structure

```
Doc Summarizer/
├── backend/
│   ├── main.py           # FastAPI app, /process endpoint
│   ├── extractor.py      # PDF (PyMuPDF) + Image (pytesseract) extraction
│   ├── summarizer.py     # Gemini AI summarization
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx                    # Main application
    │   ├── index.css                  # Premium dark design system
    │   └── components/
    │       ├── UploadZone.jsx         # Drag & drop upload
    │       └── SummaryResult.jsx     # Results display
    ├── index.html
    └── .env
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + Vite | UI framework |
| Styling | Vanilla CSS | Custom dark glassmorphism design |
| Backend | FastAPI | REST API server |
| PDF Parsing | PyMuPDF (`fitz`) | High-quality PDF text extraction |
| OCR | Tesseract + pytesseract | Image text recognition |
| AI | Google Gemini 1.5 Flash | Smart summarization |

---

## 🌐 Deployment

### Frontend → Vercel
```bash
cd frontend
npm run build
# Deploy the dist/ folder to Vercel
```

### Backend → Render
1. Push `backend/` to a GitHub repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Update `frontend/.env` → `VITE_API_URL=https://your-render-app.onrender.com`

---

## 📝 My Approach

I chose **FastAPI** for the backend due to its async capabilities and automatic OpenAPI documentation, making it easy to test endpoints during development. For text extraction, **PyMuPDF** was selected over alternatives (pdfplumber, PyPDF2) for its superior text layout preservation. **Tesseract OCR** provides free, production-quality image text recognition.

For AI summarization, **Google Gemini 1.5 Flash** offers a generous free tier with excellent instruction-following capabilities. I used structured JSON prompting to reliably extract summaries, key points, and improvement suggestions in a single API call.

The frontend uses a **premium dark glassmorphism design** with micro-animations to create a polished user experience. The API key is entered via the UI (rather than hard-coded) to ensure flexibility and security.

---

## ⚠️ Error Handling

- **Invalid API key** → Clear error message with guidance
- **Unsupported file type** → Validated on both client and server
- **File too large** (>20MB) → Rejected with size info
- **Empty/unreadable document** → Descriptive error returned
- **Backend unreachable** → User-friendly connection error
