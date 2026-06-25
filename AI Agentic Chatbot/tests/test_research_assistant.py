from research_assistant import ResearchAssistant


def test_multi_agent_workflow_returns_expected_sections():
    assistant = ResearchAssistant()
    result = assistant.run_workflow("AI in healthcare", provider="Local fallback")

    assert "summary" in result
    assert "web_results" in result
    assert "citations" in result
    assert "presentation_bytes" in result
    assert "key_points" in result
    assert "context" in result
    assert "workflow_steps" in result
    assert len(result["workflow_steps"]) >= 3


def test_workflow_creates_fallback_sources_when_web_search_is_empty(monkeypatch):
    assistant = ResearchAssistant()
    monkeypatch.setattr(assistant, "search_web", lambda query, max_results=5: [])

    result = assistant.run_workflow("AI in healthcare", provider="Local fallback")

    assert len(result["web_results"]) >= 1
    assert len(result["citations"]) >= 1
    assert "AI in healthcare" in result["summary"]


def test_clarify_query_returns_prompt_for_vague_request():
    assistant = ResearchAssistant()

    clarification = assistant.clarify_query("Tell me about AI")

    assert clarification.lower()
    assert any(word in clarification.lower() for word in ["clarify", "which", "what", "do you want"])
