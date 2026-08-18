"""Parses .vtt or plain .txt transcripts into a list of (speaker, text) turns."""

import re


def parse_vtt(filepath: str):
    """Parses a simplified WEBVTT file with 'Speaker: text' cue lines."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    turns = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines or lines[0].startswith("WEBVTT"):
            continue
        # skip the timestamp line, keep any line that looks like "Speaker: text"
        for line in lines:
            match = re.match(r"^([A-Za-z][\w .'-]{0,40}):\s*(.+)$", line)
            if match:
                speaker, text = match.group(1).strip(), match.group(2).strip()
                turns.append({"speaker": speaker, "text": text})
    return turns


def parse_txt(filepath: str):
    """Parses a plain text transcript, one 'Speaker: text' line per turn."""
    turns = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.match(r"^([A-Za-z][\w .'-]{0,40}):\s*(.+)$", line)
            if match:
                turns.append({"speaker": match.group(1).strip(), "text": match.group(2).strip()})
    return turns


def parse_transcript(filepath: str):
    if filepath.lower().endswith(".vtt"):
        return parse_vtt(filepath)
    return parse_txt(filepath)
