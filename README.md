# 📄 Doc Summarizer

An AI-powered document analysis web application that extracts text from **PDF files** and **scanned images**, then generates smart summaries with key points and improvement suggestions using **Google Gemini**.

## 🚀 Live Demo

Try the deployed application here:

**[AI Document Summarizer](https://doument-summarizer-uuzjytjx8k3awdzra3t4qg.streamlit.app/)**

Upload a PDF or image and generate an AI-powered summary with key points and improvement suggestions.

---

## ✨ Features

* 📤 **PDF and Image Upload** — Upload PDF documents or scanned images
* 📕 **PDF Text Extraction** — Extract text from PDFs using PyMuPDF
* 🖼️ **OCR Support** — Extract text from scanned images using Tesseract OCR
* 🤖 **AI-Powered Summarization** — Generate summaries using Google Gemini
* 📏 **Adjustable Summary Length** — Short, Medium, or Long
* 🎯 **Key Points** — Automatically identify important points
* 💡 **Improvement Suggestions** — Generate suggestions based on document content
* 📊 **Document Statistics** — Display word count, character count, document type, and estimated reading time
* 📥 **Download Summary** — Download the generated summary as a `.txt` file
* 🔐 **Secure API Key Handling** — API keys can be provided through Streamlit Secrets or the application interface
* 📱 **Responsive UI** — Clean and user-friendly Streamlit interface

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │   Streamlit App      │
                    │      app.py          │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
        ┌────────▼────────┐        ┌────────▼────────┐
        │    Extractor    │        │    Summarizer   │
        │  PDF / OCR      │        │  Google Gemini  │
        └────────┬────────┘        └────────┬────────┘
                 │                           │
        ┌────────▼────────┐        ┌────────▼────────┐
        │    PyMuPDF      │        │  Gemini API     │
        │   Tesseract     │        │  AI Processing  │
        └─────────────────┘        └─────────────────┘
```

The Streamlit application acts as the main interface and connects directly to the Python modules inside the `backend` directory.

---

## 🛠️ Tech Stack

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| Streamlit         | Web application and user interface  |
| Python            | Core programming language           |
| PyMuPDF (`fitz`)  | PDF text extraction                 |
| Tesseract OCR     | Text extraction from scanned images |
| pytesseract       | Python interface for Tesseract      |
| Pillow            | Image processing                    |
| Google Gemini API | AI-powered document summarization   |
| python-dotenv     | Environment variable management     |

---

## 📁 Project Structure

```text
Doc Summarizer/
│
├── backend/
│   ├── extractor.py       # PDF and image text extraction
│   ├── main.py            # FastAPI backend module
│   ├── summarizer.py      # Gemini AI summarization
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Environment variable example
│
├── frontend/
│   └── ...                # Original frontend files
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Streamlit deployment dependencies
├── packages.txt           # Linux system packages for deployment
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

---

## ⚙️ How It Works

The application follows these steps:

```text
1. User uploads a PDF or image
                ↓
2. File type is identified
                ↓
3. PDF → PyMuPDF text extraction
   Image → Tesseract OCR
                ↓
4. Extracted text is validated
                ↓
5. Text is sent to Google Gemini
                ↓
6. Gemini generates:
      • Executive Summary
      • Key Points
      • Improvement Suggestions
                ↓
7. Results are displayed
                ↓
8. User can download the summary
```

---

## 🚀 Running Locally

### Prerequisites

Make sure you have:

| Tool          | Recommended Version |
| ------------- | ------------------- |
| Python        | 3.9+                |
| Tesseract OCR | 5.x                 |
| pip           | Latest version      |

### 1. Clone the repository

```bash
git clone https://github.com/pavankarthik11/doument-summarizer.git
cd doument-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

#### Windows

Download and install Tesseract OCR from:

https://github.com/UB-Mannheim/tesseract/wiki

The default installation location is usually:

```text
C:\Program Files\Tesseract-OCR\
```

Add the Tesseract installation directory to your system PATH if required.

#### macOS

```bash
brew install tesseract
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 5. Run the Streamlit application

```bash
python -m streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## 🔑 Google Gemini API Key

The application requires a Google Gemini API key for AI summarization.

### Get an API key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account.
3. Create an API key.
4. Copy the generated key.
5. Enter it in the application's **Gemini API Key** field.

### Streamlit Deployment

For Streamlit Community Cloud, the API key should be stored using **Streamlit Secrets**:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

The API key should **never be committed to GitHub**.

---

## 🌐 Deployment

The application is deployed using **Streamlit Community Cloud**.

### Live Application

**[Open AI Document Summarizer](https://doument-summarizer-uuzjytjx8k3awdzra3t4qg.streamlit.app/)**

### Deployment Configuration

```text
Repository:
pavankarthik11/doument-summarizer

Branch:
main

Main file:
app.py

Python:
3.12
```

The project uses:

```text
requirements.txt
```

for Python dependencies and:

```text
packages.txt
```

for required Linux system packages such as Tesseract OCR.

---

## 📄 Supported File Formats

### PDF

```text
.pdf
```

PDF text is extracted using **PyMuPDF**.

### Images

```text
.png
.jpg
.jpeg
.webp
.bmp
.tiff
```

Image text is extracted using **Tesseract OCR**.

### File Size

The application currently supports files up to:

```text
20 MB
```

---

## 📊 Summary Output

After processing a document, the application provides:

### Executive Summary

A concise overview of the document.

### Key Points

Important information extracted from the document.

### Improvement Suggestions

AI-generated suggestions based on the document content.

### Document Statistics

The application also displays:

* Document type
* Word count
* Character count
* Estimated reading time

---

## 📝 Summary Length

Users can choose from three summary lengths:

| Option | Description      |
| ------ | ---------------- |
| Short  | Brief summary    |
| Medium | Balanced summary |
| Long   | Detailed summary |

---

## 💾 Download Summary

After generating the summary, users can download the result as a text file:

```text
Summary of <filename>.txt
```

The downloaded file contains:

```text
Executive Summary
        ↓
Key Points
        ↓
Improvement Suggestions
```

---

## 🛡️ Error Handling

The application handles several common errors:

* ❌ Missing Gemini API key
* ❌ Invalid or unsupported file type
* ❌ File size exceeding 20 MB
* ❌ Empty or unreadable document
* ❌ PDF extraction failure
* ❌ OCR extraction failure
* ❌ Gemini API errors
* ❌ Corrupted documents

Users receive clear error messages when a problem occurs.

---

## 🔐 Security

Sensitive information such as API keys is not stored directly in the source code.

The project uses:

```text
.env
```

for local environment variables and **Streamlit Secrets** for cloud deployment.

The `.gitignore` file prevents sensitive files such as `.env` and virtual environments from being committed to GitHub.

**Never commit API keys or passwords to a public repository.**

---

## 🧠 My Approach

The project was designed to provide a simple way to analyze documents using artificial intelligence.

For PDF documents, **PyMuPDF** was selected because it provides efficient and reliable text extraction while preserving useful document information.

For scanned images, **Tesseract OCR** is used to recognize and extract text from image content.

After text extraction, the content is sent to **Google Gemini**, which generates a structured response containing:

```text
Executive Summary
Key Points
Improvement Suggestions
```

The Streamlit interface was chosen because it allows the document processing functionality to be presented through a simple and interactive web application without requiring a separate frontend deployment.

---

## 🎯 Project Goals

The main goals of the project are:

1. Make document summarization simple and accessible.
2. Support both digital PDFs and scanned documents.
3. Extract useful information automatically.
4. Reduce the time required to read lengthy documents.
5. Provide structured AI-generated summaries.
6. Give users important points and improvement suggestions.
7. Provide a simple web interface that can be accessed online.

---

## 🚀 Future Enhancements

Possible future improvements include:

* 📑 Support for DOCX and PPTX files
* 🌍 Multi-language OCR and summarization
* 🔊 Text-to-speech summaries
* 💬 Interactive document chat
* 📚 Multiple document comparison
* 📊 Advanced document analytics
* 📥 PDF summary export
* 👤 User accounts and document history
* ☁️ Cloud-based document storage

---

## 👨‍💻 Project

**Doc Summarizer**

An AI-powered document analysis application built using Python, Streamlit, Tesseract OCR, PyMuPDF, and Google Gemini.

### 🔗 Links

* **Live Demo:** https://doument-summarizer-uuzjytjx8k3awdzra3t4qg.streamlit.app/
* **GitHub Repository:** https://github.com/pavankarthik11/doument-summarizer

---

⭐ If you find this project useful, consider giving the repository a star!
