# Agentic AI Research Assistant

A polished Streamlit app for researching a topic, generating a clear summary, collecting sources, building citations, and exporting a presentation.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repository to GitHub.
2. Open Streamlit Cloud and create a new app from that GitHub repository.
3. Set the main file to app.py.
4. Add the packages from requirements.txt.

## Optional API keys

Create a .env file with:

```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

If no API key is provided, the app uses a local fallback workflow.
