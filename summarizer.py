# not implimented 
# need to update it later

import os


def _rule_based_summary(turns):
    """Naive fallback: picks the first line from each speaker's longest turn
    and joins them into bullet points. Not smart, but deterministic and
    good enough to exercise the rest of the pipeline without an API key."""
    speaker_best_line = {}
    for turn in turns:
        s, t = turn["speaker"], turn["text"]
        if s not in speaker_best_line or len(t) > len(speaker_best_line[s]):
            speaker_best_line[s] = t

    bullets = [f"- {speaker}: {line}" for speaker, line in speaker_best_line.items()]
    return "Meeting Summary (local fallback, no LLM configured):\n" + "\n".join(bullets)





def summarize(turns):
    """Returns a summary string. Falls back gracefully if no API key or
    the API call fails, so this always returns something usable."""
    if os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT"):
        try:
            return _azure_openai_summary(turns)
        except Exception as e:
            return _rule_based_summary(turns) + f"\n\n[Note: Azure OpenAI call failed ({e}), used fallback]"
    return _rule_based_summary(turns)
