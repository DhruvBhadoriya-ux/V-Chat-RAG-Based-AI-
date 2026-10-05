# V-CHAT RAG Based AI

> An AI-powered educational chatbot that helps students ask questions about course lectures and receive grounded answers with lecture and timestamp references.

---

## 📌 Overview

**V-CHAT RAG Based AI** is an educational AI chatbot designed to help students interact with their course lecture content using natural-language questions.

Instead of searching through long lecture videos manually, students can ask questions such as:

> "What is the difference between HTML tags and attributes?"

V-CHAT processes the question, searches the relevant lecture content using **Retrieval-Augmented Generation (RAG)**, and generates an answer based on the retrieved lecture material.

The system can also provide:

* 📚 Lecture/source references
* 🎥 Video numbers
* ⏱️ Approximate timestamps
* 🤖 AI-generated explanations
* 💬 Chat-based interaction
* 🎙️ Planned voice interaction
* 📁 Planned document and lecture upload support

The current project consists of a **React frontend**, **FastAPI backend**, and a local **RAG pipeline powered by Ollama**.

---

## ✨ Features

### Currently Implemented

#### 🤖 RAG-Based Question Answering

Students can ask natural-language questions about the available lecture content.

The system:

1. Receives the student's question.
2. Converts the question into an embedding.
3. Searches the lecture embeddings using cosine similarity.
4. Retrieves the most relevant lecture chunks.
5. Sends the retrieved context to the LLM.
6. Generates a grounded answer.

#### 🔎 Semantic Search

V-CHAT uses embeddings rather than simple keyword matching.

* Embedding model: `bge-m3`
* Similarity measure: Cosine Similarity
* Retrieval: **top 5 most relevant chunks**

#### 🎥 Lecture References

The RAG system stores lecture metadata such as:

* Lecture/video title
* Video number
* Start timestamp
* End timestamp
* Transcript text

The frontend displays this information as **Lecture Sources** below the AI response.

Example:

```text
Lecture Sources

HTML Basics
Video 1 • 00:15 - 00:32
```

#### 💬 Chat Interface

The frontend provides a chatbot-style interface with:

* New Chat
* Conversation history
* User messages
* AI messages
* AI typing state
* Lecture source cards
* Timestamp information
* Responsive layout

#### 🔌 Frontend–Backend Integration

The React frontend communicates with the FastAPI backend through a REST API.

Current endpoint:

```http
POST /ask
```

Example request:

```json
{
  "question": "What is HTML?"
}
```

Example response:

```json
{
  "answer": "HTML is ...",
  "sources": [
    {
      "title": "Your First HTML Website",
      "video_number": 1,
      "start": 15.0,
      "end": 32.0,
      "start_time": "00:15",
      "end_time": "00:32"
    }
  ]
}
```

---

## 🧠 How V-CHAT Works

```text
                Student
                   │
                   ▼
          ┌──────────────────┐
          │  React Frontend  │
          └────────┬─────────┘
                   │ Question
                   ▼
          ┌──────────────────┐
          │  FastAPI Backend │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Question         │
          │ Embedding        │
          │ (bge-m3)         │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Similarity Search│
          │ (Cosine)         │
          └────────┬─────────┘
                   │ Top 5 Chunks
                   ▼
          ┌──────────────────┐
          │ Retrieved        │
          │ Lecture Context  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Llama 3          │
          │ Generation       │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Answer + Sources │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  React Chat UI   │
          └──────────────────┘
```

---

## 🏗️ Project Architecture

```text
V-CHAT/
│
├── Backend/
│   ├── audios/
│   ├── jsons/
│   ├── videos/
│   ├── whisper/
│   │
│   ├── embeddings.joblib
│   │
│   ├── Mp3_to_json.py
│   ├── process_incoming.py
│   ├── read_chunks.py
│   ├── video_to_mp3.py
│   │
│   ├── api.py
│   └── rag_engine.py
│
├── Frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── ChatArea.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── Icons.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── mockData.js
│   ├── package.json
│   └── ...
│
└── README.md
```

---

## ⚙️ Technology Stack

### Frontend

| Technology | Purpose                |
| ---------- | ---------------------- |
| React      | Frontend UI            |
| JavaScript | Application logic      |
| Vite       | Development/build tool |
| CSS        | Styling                |
| Fetch API  | Backend communication  |

### Backend

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python       | Backend/RAG implementation |
| FastAPI      | REST API                   |
| Uvicorn      | API server                 |
| Pydantic     | Request validation         |
| Pandas       | Data processing            |
| NumPy        | Numerical operations       |
| Scikit-learn | Cosine similarity          |
| Joblib       | Embedding storage/loading  |
| Requests     | Communication with Ollama  |

### AI / RAG

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| Ollama            | Local AI model serving              |
| BGE-M3            | Text embeddings                     |
| Llama 3           | Answer generation                   |
| RAG               | Lecture-grounded question answering |
| Cosine Similarity | Semantic retrieval                  |

---

## 📂 Backend Components

| File                 | Description |
| -------------------- | ----------- |
| `api.py`             | FastAPI server exposing `POST /ask`; passes the question to the RAG engine. |
| `rag_engine.py`      | Main RAG module: embedding → similarity calculation → top 5 chunks → context creation → Llama 3 → answer + sources. Embeddings are loaded once at server start. |
| `embeddings.joblib`  | Pre-generated embeddings and lecture metadata (`title`, `number`, `start`, `end`, `text`, `embedding`). |
| `video_to_mp3.py`    | Extracts audio from video content. |
| `Mp3_to_json.py`     | Converts audio/transcription output into structured JSON. |
| `read_chunks.py`     | Reads and processes lecture chunks before embedding/retrieval. |
| `process_incoming.py`| Original local RAG script used for testing before the FastAPI integration. |

The production-style API flow is handled through:

```text
api.py → rag_engine.py
```

---

## 🖥️ Frontend Components

| Component         | Responsibility |
| ----------------- | -------------- |
| `App.jsx`         | Main component: manages conversations, creates/selects chats, sends questions, calls the FastAPI backend, receives answers and sources, manages the AI typing state. |
| `Sidebar.jsx`     | V-CHAT branding, New Chat, chat history, conversation selection. |
| `ChatArea.jsx`    | Controls the main conversation area. |
| `ChatInput.jsx`   | Question input and microphone UI. |
| `ChatMessage.jsx` | Displays user/AI messages, timestamps, and lecture source information. |

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.10+
* Node.js
* npm
* Ollama
* Git

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd V-CHAT
```

### 2. Set Up Ollama

Install Ollama and download the required models:

```bash
ollama pull bge-m3
ollama pull llama3
```

Make sure Ollama is running before starting the backend. Verify with:

```bash
ollama list
```

### 3. Set Up the Backend

```bash
cd Backend
python -m pip install fastapi uvicorn pandas numpy scikit-learn joblib requests
python -m uvicorn api:app --reload
```

The backend runs at `http://127.0.0.1:8000`. Visiting the root should return:

```json
{
  "message": "V-CHAT API is running!"
}
```

### 4. Set Up the Frontend

In another terminal:

```bash
cd Frontend
npm install
npm run dev
```

Vite will provide a local URL similar to `http://localhost:5173`.

---

## 🔄 Running the Complete Project

You need **two terminals**.

**Terminal 1 — Backend**

```bash
cd Backend
python -m uvicorn api:app --reload
```

**Terminal 2 — Frontend**

```bash
cd Frontend
npm run dev
```

Then open `http://localhost:5173`.

---

## 🧪 Testing the API

You can test the backend without the frontend:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is HTML?"}'
```

Expected response shape:

```json
{
  "answer": "...",
  "sources": [
    {
      "title": "...",
      "video_number": 1,
      "start": 100.0,
      "end": 130.0,
      "start_time": "01:40",
      "end_time": "02:10"
    }
  ]
}
```

---

## 🔐 Environment Variables

If the project later requires API keys, database credentials, or other secrets, store them in a `.env` file and **never commit it to GitHub**.

---

## 🚫 Recommended `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
env/

# Environment variables
.env

# Node
node_modules/
dist/

# macOS
.DS_Store

# IDE
.vscode/
.idea/

# Logs
*.log

# Temporary files
tempCodeRunnerFile.py

# Generated outputs
response.txt
prompt.txt
```

---

## 📊 RAG Pipeline

1. **User Question** — e.g. "What is the purpose of HTML?"
2. **Question Embedding** — converted to a vector using BGE-M3.
3. **Similarity Search** — compared with stored lecture vectors using cosine similarity.
4. **Top-K Retrieval** — the five most relevant chunks are selected.
5. **Context Construction** — retrieved chunks are passed to the language model with the question.
6. **Answer Generation** — Llama 3 generates the response from the lecture context.
7. **Source Information** — the backend returns lecture title, video number, start and end timestamps.
8. **Frontend Display** — the React interface shows the answer and lecture sources.

---

## 🎯 Example Interaction

**Student**

```text
What are HTML tags?
```

**V-CHAT**

```text
HTML tags are keywords enclosed in angle brackets that define
the structure and elements of an HTML document.

This topic is covered in the lecture:
Your First HTML Website

Lecture Sources:
Video 1 • 12:40 - 13:25
```

This helps the student understand the answer and find where the concept appears in the lecture.

---

## 🎓 Intended Educational Use

V-CHAT is designed for educational environments where students have access to recorded lectures or course materials.

```text
University LMS
      │
      ▼
Lecture Upload
      │
      ▼
Audio / Video Processing
      │
      ▼
Speech-to-Text
      │
      ▼
Transcript Chunking
      │
      ▼
BGE-M3 Embeddings
      │
      ▼
Knowledge Base
      │
      ▼
V-CHAT
      │
      ▼
Student Questions
```

---

## 🔮 Future Development

* **🎙️ Voice Interaction** — ask questions via microphone using speech-to-text.
* **📁 Lecture and File Upload** — support PDF, PPT/PPTX, audio, video, and lecture notes.
* **🔄 Automatic Lecture Processing** — new lectures automatically flow through detection → audio extraction → speech-to-text → chunking → embeddings → knowledge base update.
* **⏱️ Clickable Lecture Timestamps** — e.g. clicking `Video 2 • 12:45` opens the lecture at that point.
* **🗄️ Database Integration** — store user accounts, chat history, search history, and uploaded content metadata (MongoDB under consideration).
* **👥 User Authentication** — login, personal chat history, personalized V-CHAT, with securely hashed passwords.
* **🧠 Improved Retrieval** — move from Joblib + cosine similarity to a vector database such as FAISS, Chroma, Qdrant, Pinecone, or MongoDB Vector Search.
* **🏫 University LMS Integration** — let students ask questions directly about lectures in their courses.

---

## 📈 Current vs Future System

| Feature                     | Status                       |
| --------------------------- | ---------------------------- |
| React frontend              | ✅ Implemented                |
| FastAPI backend             | ✅ Implemented                |
| Ollama integration          | ✅ Implemented                |
| BGE-M3 embeddings           | ✅ Implemented                |
| Llama 3 generation          | ✅ Implemented                |
| Cosine similarity retrieval | ✅ Implemented                |
| Top-5 retrieval             | ✅ Implemented                |
| Lecture source information  | ✅ Implemented                |
| Timestamp display           | ✅ Implemented                |
| Chat interface              | ✅ Implemented                |
| Voice input                 | 🔄 Planned / Under development |
| File upload                 | 🔄 Planned                    |
| MongoDB chat history        | 🔄 Planned                    |
| User authentication         | 🔄 Planned                    |
| Clickable timestamps        | 🔄 Planned                    |
| Automatic LMS ingestion     | 🔄 Planned                    |
| University LMS integration  | 🔄 Planned                    |
| Production vector database  | 🔄 Planned                    |

---

## 🛡️ Important Notes

V-CHAT generates answers from the lecture content retrieved by the RAG pipeline. Response quality depends on:

* Quality of the lecture transcript
* Quality of chunking
* Embedding quality
* Retrieval accuracy
* Language model output

For production deployment, add validation, authentication, security, monitoring, and error handling.

---

## 📌 Project Status

**Current Status: Working Prototype**

```text
React Frontend
      ↕
FastAPI API
      ↕
RAG Engine
      ↕
BGE-M3
      ↕
Lecture Embeddings
      ↕
Llama 3
```

The system receives a student question, retrieves relevant lecture content, generates an AI response, and displays the associated lecture sources and timestamps.

---

## 👨‍💻 Developer

**Dhruv Bhadoriya**
B.Tech Computer Science Engineering — Data Science & Machine Learning

---

## 📄 License

This project is currently intended for educational and academic purposes. A formal open-source license can be added when the project is ready for public distribution.

---

## ⭐ Acknowledgement

This project explores the use of **Retrieval-Augmented Generation (RAG)** to improve access to educational lecture content, making recorded lectures easier to search, understand, and navigate using natural language.
