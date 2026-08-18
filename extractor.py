"""Extracts action items, owners, and due dates from transcript turns.

This is intentionally rule-based and imperfect (mirrors a realistic partial
hackathon submission): it catches explicit commitments ("I'll do X by Friday")
well, but misses implicit asks and often falls back to a placeholder due date.
"""

import re

COMMITMENT_PATTERNS = [
    r"\bI'?ll\s+(.+)",
    r"\bI\s+will\s+(.+)",
    r"\bI\s+can\s+(take|do|handle)\s+(.+)",
]

WEAK_SIGNAL_PATTERNS = [
    r"\bsomeone should\b",
    r"\bwe should\b",
    r"\bwe need\b",
]

DUE_DATE_PATTERNS = [
    (r"\bby\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", "explicit_day"),
    (r"\bby\s+(end of week|eow)\b", "explicit_eow"),
    (r"\bby\s+(next\s+\w+)\b", "explicit_relative"),
]


def _find_due_date(text: str):
    text_lower = text.lower()
    for pattern, kind in DUE_DATE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1).title(), kind
    return "End of week", "default_placeholder"  # weak fallback, intentionally


def extract_action_items(turns):
    items = []
    flagged_weak_signals = []

    for i, turn in enumerate(turns):
        speaker, text = turn["speaker"], turn["text"]

        matched_commitment = False
        for pattern in COMMITMENT_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                due_date, due_kind = _find_due_date(text)
                items.append({
                    "description": text,
                    "owner": speaker,
                    "owner_confidence": "high",
                    "due_date": due_date,
                    "due_date_confidence": "high" if due_kind.startswith("explicit") else "low",
                    "source_turn": i,
                })
                matched_commitment = True
                break

        if not matched_commitment:
            for pattern in WEAK_SIGNAL_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE):
                    # implicit ask with no clear owner - flagged, not auto-added
                    # (this is the known gap: these get missed unless a human
                    # later assigns an owner explicitly, e.g. "Rachel, can you own that")
                    flagged_weak_signals.append({"text": text, "speaker": speaker, "source_turn": i})
                    break

    return items, flagged_weak_signals
