from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI(title="Sentiment Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_SENTIMENTS = {"positive", "negative", "neutral"}

def extract_sentiment(raw: str) -> str:
    """Parse Mistral's response and return a clean sentiment label."""
    cleaned = raw.strip().lower()
    for label in VALID_SENTIMENTS:
        if label in cleaned:
            return label.capitalize()
    # Fallback: return the first word if model went off-script
    first_word = re.split(r"[\s.,!?]", cleaned)[0]
    return first_word.capitalize() if first_word else "Unknown"

@app.get("/")
def root():
    return {"message": "Sentiment Analyzer API is running!"}

@app.post("/analyze/")
def analyze_sentiment(text: str = Form(...)):
    prompt = (
        "Analyze the sentiment of the following text. "
        "Respond with exactly one word — either Positive, Negative, or Neutral. "
        "Do not add any explanation.\n\n"
        f"Text: {text}"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        result = response.json()
        raw_response = result.get("response", "")
        sentiment = extract_sentiment(raw_response)
        return {"sentiment": sentiment, "raw": raw_response.strip()}

    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to Ollama. Make sure it is running on port 11434."}
    except Exception as e:
        return {"error": str(e)}
