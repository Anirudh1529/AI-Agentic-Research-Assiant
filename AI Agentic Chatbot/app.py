import os
import time

import streamlit as st
from dotenv import load_dotenv

from research_assistant import ResearchAssistant

load_dotenv()

st.set_page_config(page_title="Agentic AI Research Assistant", page_icon="🧠", layout="wide")

st.markdown(
    """
    <style>
    :root { color-scheme: light; }
    .stApp { background: linear-gradient(135deg, #f8fbff 0%, #f3f7ff 45%, #eef4ff 100%); color: #14213d; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e5ebf5; }
    .hero { padding: 1.5rem 1.6rem; border-radius: 24px; background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%); border: 1px solid #e6ecf7; box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06); margin-bottom: 1rem; }
    .hero h1 { font-size: 2.05rem; margin-bottom: 0.35rem; font-weight: 700; color: #14213d; }
    .hero p { color: #4b5d7a; font-size: 1rem; }
    .panel { padding: 1rem 1.1rem; border-radius: 20px; background: #ffffff; border: 1px solid #e8edf7; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04); margin-bottom: 1rem; }
    .card { border-radius: 18px; padding: 1rem; background: #fcfdff; border: 1px solid #e8edf7; height: 100%; box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04); }
    .chip { display: inline-block; padding: 0.28rem 0.6rem; border-radius: 999px; background: #e8f2ff; color: #2563eb; font-size: 0.8rem; margin-bottom: 0.5rem; font-weight: 600; }
    .result-card { padding: 0.9rem 1rem; border-radius: 16px; background: #f8fbff; border: 1px solid #e8edf7; margin-bottom: 0.7rem; }
    .metric-card { padding: 0.8rem 0.9rem; border-radius: 16px; background: #f8fbff; border: 1px solid #e8edf7; margin-bottom: 0.6rem; }
    .chat-shell { padding: 0.95rem; border-radius: 20px; background: #ffffff; border: 1px solid #e8edf7; margin-top: 1rem; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04); }
    .chat-bubble { padding: 0.7rem 0.85rem; border-radius: 14px; margin-bottom: 0.55rem; background: #eef5ff; color: #14213d; border: 1px solid #dce8ff; }
    .user-bubble { background: #f8fbff; border: 1px solid #e8edf7; }
    .stButton > button { border-radius: 999px; padding: 0.6rem 1rem; background: linear-gradient(90deg, #2563eb, #3b82f6); color: white; border: none; box-shadow: 0 6px 16px rgba(37, 99, 235, 0.18); }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] { border-radius: 12px; border: 1px solid #dce8ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

assistant = ResearchAssistant()

if "result" not in st.session_state:
    st.session_state.result = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I can help you research a topic, summarize papers, collect sources, and prepare a presentation. Tell me your topic or ask for a specific goal.",
        }
    ]


def run_workflow_for_topic(topic_value: str, uploaded_file_bytes, provider_value: str, api_key_value: str):
    with st.spinner("Gathering context and preparing a polished answer..."):
        result = assistant.run_workflow(
            topic=topic_value,
            pdf_bytes=uploaded_file_bytes,
            provider=provider_value,
            api_key=api_key_value,
        )
    st.session_state.result = result
    st.session_state.last_topic = topic_value
    return result


def render_results(result: dict, topic: str) -> None:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Research results")
    st.success("A polished research package is ready.")
    st.caption(f"Topic: {topic}")

    st.markdown("### Workflow stages")
    for step in result.get("workflow_steps", []):
        st.write(f"- {step}")

    tab_summary, tab_sources, tab_citations, tab_presentation = st.tabs(["Summary", "Sources", "Citations", "Presentation"])

    with tab_summary:
        st.markdown("**Research summary**")
        st.write(result.get("summary", "No summary available."))
        st.markdown("**Key points**")
        for point in result.get("key_points", []):
            st.write(f"- {point}")

    with tab_sources:
        web_results = result.get("web_results", [])
        if web_results:
            for item in web_results:
                st.markdown(
                    f"<div class='result-card'><strong>{item.get('title', 'Source')}</strong><br>{item.get('snippet', '')}<br><a href='{item.get('url', '#')}' target='_blank'>{item.get('url', '#')}</a></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No sources were returned for this run.")

    with tab_citations:
        citations = result.get("citations", [])
        if citations:
            for index, citation in enumerate(citations, start=1):
                st.write(f"{index}. {citation}")
        else:
            st.info("No citations were generated for this run.")

    with tab_presentation:
        presentation_bytes = result.get("presentation_bytes")
        if presentation_bytes:
            st.download_button(
                "Download presentation",
                data=presentation_bytes,
                file_name="research_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
            )
            st.caption("This presentation includes the summary and highlights generated for this run.")
        else:
            st.info("No presentation file was generated for this run.")
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="hero">
      <span class="chip">⚡ Agentic AI Research Assistant</span>
      <h1>Research, summarize, and present with clarity</h1>
      <p>Built for fast, relevant answers with a simple flow for topic exploration, summaries, citations, and presentation export.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Setup")
    provider = st.selectbox("LLM provider", ["Local fallback", "OpenAI", "Gemini"], index=0)
    if provider == "OpenAI":
        api_key = st.text_input("OpenAI API key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    elif provider == "Gemini":
        api_key = st.text_input("Gemini API key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    else:
        api_key = ""

    st.divider()
    st.markdown("<div class='metric-card'><strong>🧠 Assistant mode</strong><br>Research-focused and easy to follow.</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-card'><strong>⚡ Speed</strong><br>Fast local fallback for quick results.</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-card'><strong>📄 PDFs</strong><br>Upload a PDF when you want more context.</div>", unsafe_allow_html=True)

st.markdown("<div class='panel'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom: 0.4rem;'>Start a research run</h3>", unsafe_allow_html=True)
col_topic, col_upload = st.columns([2, 1])
with col_topic:
    topic = st.text_input("Research topic", value=st.session_state.last_topic, placeholder="e.g. AI in healthcare")
with col_upload:
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
submitted = st.button("Run workflow", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic to research.")
        st.stop()
    run_workflow_for_topic(topic, uploaded_file.getvalue() if uploaded_file else None, provider, api_key)

st.markdown("<div class='chat-shell'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom: 0.4rem;'>Assistant chat</h3>", unsafe_allow_html=True)
for message in st.session_state.messages:
    bubble_class = "chat-bubble user-bubble" if message["role"] == "user" else "chat-bubble"
    st.markdown(f"<div class='{bubble_class}'><strong>{message['role'].title()}</strong><br>{message['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Ask a question or paste a topic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    lower_prompt = prompt.strip().lower()

    if any(word in lower_prompt for word in ["hello", "hi", "hey", "what can you do", "help"]):
        reply = "I can help you research a topic, summarize papers, find sources, create citations, and prepare a presentation. Tell me your topic or what you want to achieve."
    else:
        clarification = assistant.clarify_query(prompt)
        if clarification:
            reply = clarification
        else:
            with st.spinner("Preparing a focused response..."):
                result = run_workflow_for_topic(prompt, None, provider, api_key)
            reply = f"I’ve prepared a draft for '{prompt}'. Review the summary, sources, citations, and presentation below."
            if result.get("summary"):
                reply = f"I’ve prepared a draft for '{prompt}'. The summary and supporting material are ready below."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.result:
    render_results(st.session_state.result, st.session_state.last_topic)
else:
    st.markdown(
        """
        <div class='panel'>
          <h3>Ready to begin</h3>
          <p>Enter a topic, optionally upload a PDF, and I’ll prepare a clear research summary with sources and a presentation-ready output.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
