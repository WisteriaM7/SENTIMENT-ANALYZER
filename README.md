# 🎭 Sentiment Analyzer (Mistral)

An AI-powered text sentiment classification app using a **locally hosted Mistral model** via Ollama, with a FastAPI backend and a Streamlit frontend.

---

## 🧠 Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| LLM       | Mistral (via Ollama)    |
| Backend   | FastAPI + Uvicorn       |
| Frontend  | Streamlit               |
| Language  | Python 3.10+            |

---

## 📁 Project Structure

```
sentiment-analyzer-mistral/
│
├── backend/
│   ├── __init__.py
│   └── main.py          # FastAPI app with /analyze/ endpoint
│
├── frontend/
│   └── app.py           # Streamlit UI
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sentiment-analyzer-mistral.git
cd sentiment-analyzer-mistral
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama & Pull the Mistral Model

- Download Ollama from: https://ollama.com
- Pull the model:

```bash
ollama pull mistral
```

---

## 🚀 Running the App

Open **two separate terminals**:

**Terminal 1 — Start the Backend:**

```bash
uvicorn backend.main:app --reload
```

Backend runs at: `http://localhost:8000`

**Terminal 2 — Start the Frontend:**

```bash
streamlit run frontend/app.py
```

Frontend runs at: `http://localhost:8501`

---

## 📌 API Endpoints

| Method | Endpoint    | Description                              |
|--------|-------------|------------------------------------------|
| GET    | `/`         | Health check                             |
| POST   | `/analyze/` | Classify text as Positive/Negative/Neutral |

### Example Request

```bash
curl -X POST http://localhost:8000/analyze/ \
  -F "text=I absolutely loved the movie, it was fantastic!"
```

### Example Response

```json
{
  "sentiment": "Positive",
  "raw": "Positive"
}
```

---

## ✅ Features

- Local LLM inference — no API keys or internet required
- Sentiment parsed robustly even if Mistral adds extra words
- Color-coded Streamlit UI (green / red / blue per label)
- Raw model response visible via expandable section
- CORS-enabled FastAPI backend

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| Backend not connecting | Run `uvicorn backend.main:app --reload` |
| Ollama errors | Run `ollama serve` and verify with `ollama list` |
| Sentiment shows "Unknown" | Mistral gave an unexpected response — check the raw output expander |
| Slow responses | Mistral runs locally; speed depends on your hardware |
