import streamlit as st
import requests

st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎭",
    layout="centered"
)

SENTIMENT_CONFIG = {
    "Positive": {"emoji": "😊", "color": "success", "label": "Positive"},
    "Negative": {"emoji": "😞", "color": "error",   "label": "Negative"},
    "Neutral":  {"emoji": "😐", "color": "info",    "label": "Neutral"},
}

st.title("🎭 Sentiment Analyzer")
st.markdown("Powered by **Mistral via Ollama** · FastAPI backend · Streamlit frontend")
st.divider()

text_input = st.text_area(
    "Enter your sentence or paragraph:",
    placeholder="e.g. 'The product was amazing and exceeded all expectations!'",
    height=180
)

col1, col2 = st.columns([1, 4])
with col1:
    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
with col2:
    if st.button("Clear", use_container_width=True):
        st.rerun()

if analyze_btn:
    if not text_input.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing sentiment..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze/",
                    data={"text": text_input},
                    timeout=90
                )
                result = response.json()

                if "error" in result:
                    st.error(f"❌ {result['error']}")
                else:
                    sentiment = result.get("sentiment", "Unknown")
                    config = SENTIMENT_CONFIG.get(sentiment, {
                        "emoji": "🤔", "color": "warning", "label": sentiment
                    })

                    st.divider()
                    st.subheader("🔍 Result")

                    metric_col, _ = st.columns([1, 2])
                    with metric_col:
                        st.metric(
                            label="Predicted Sentiment",
                            value=f"{config['emoji']} {config['label']}"
                        )

                    if config["color"] == "success":
                        st.success(f"The text carries a **{config['label']}** sentiment.")
                    elif config["color"] == "error":
                        st.error(f"The text carries a **{config['label']}** sentiment.")
                    else:
                        st.info(f"The text carries a **{config['label']}** sentiment.")

                    with st.expander("See raw model response"):
                        st.code(result.get("raw", "N/A"))

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Make sure FastAPI is running on port 8000.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

st.divider()
st.caption("Ensure Ollama is running (`ollama serve`) and the backend is active (`uvicorn backend.main:app --reload`).")
