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


# def _azure_openai_summary(turns):
#     import requests

#     endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
#     api_key = os.environ.get("AZURE_OPENAI_API_KEY")
#     deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

#     transcript_text = "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
#     prompt = (
#         "Summarize the following meeting transcript in 4-6 concise bullet points, "
#         "covering decisions made and topics discussed. Do not include action items "
#         "(those are handled separately).\n\n" + transcript_text
#     )

#     url = f"{endpoint}openai/deployments/{deployment}/chat/completions?api-version=2024-02-15-preview"
#     headers = {"api-key": api_key, "Content-Type": "application/json"}
#     payload = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 400}

#     resp = requests.post(url, headers=headers, json=payload, timeout=20)
#     resp.raise_for_status()
#     return resp.json()["choices"][0]["message"]["content"]


def summarize(turns):
    """Returns a summary string. Falls back gracefully if no API key or
    the API call fails, so this always returns something usable."""
    if os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT"):
        try:
            return _azure_openai_summary(turns)
        except Exception as e:
            return _rule_based_summary(turns) + f"\n\n[Note: Azure OpenAI call failed ({e}), used fallback]"
    return _rule_based_summary(turns)
