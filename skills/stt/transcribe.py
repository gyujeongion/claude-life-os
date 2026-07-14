#!/usr/bin/env python3
"""Minimal speech-to-text via Deepgram, speaker-labelled.

Bring your own key:  export DEEPGRAM_API_KEY="..."
Usage:
    python3 transcribe.py "meeting.m4a" --lang ko
    python3 transcribe.py "lecture.mp3" --lang en --no-diarize
    python3 transcribe.py "call.wav" --model nova-2

Writes "<path>.txt" next to the source and prints the transcript to stdout.
Dependencies: requests  (pip install requests)
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

API_URL = "https://api.deepgram.com/v1/listen"
CONTENT_TYPES = {
    ".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".mp4": "audio/mp4",
    ".wav": "audio/wav", ".flac": "audio/flac", ".aac": "audio/aac",
    ".ogg": "audio/ogg", ".opus": "audio/opus", ".webm": "audio/webm",
}


def transcribe(path: Path, lang: str, model: str, diarize: bool) -> str:
    key = os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        sys.exit("Set DEEPGRAM_API_KEY in your environment (see the skill's Setup step).")

    params = {
        "model": model,
        "language": lang,
        "diarize": "true" if diarize else "false",
        "punctuate": "true",
        "smart_format": "true",
    }
    headers = {
        "Authorization": f"Token {key}",
        "Content-Type": CONTENT_TYPES.get(path.suffix.lower(), "audio/mpeg"),
    }
    with path.open("rb") as f:
        resp = requests.post(API_URL, params=params, headers=headers, data=f, timeout=600)
    if resp.status_code != 200:
        sys.exit(f"Deepgram error {resp.status_code}: {resp.text[:500]}")

    return format_transcript(resp.json(), diarize)


def format_transcript(payload: dict, diarize: bool) -> str:
    """Group words by speaker into readable, labelled paragraphs."""
    try:
        alt = payload["results"]["channels"][0]["alternatives"][0]
    except (KeyError, IndexError):
        return "(no transcript returned)"

    words = alt.get("words") or []
    if not diarize or not words or "speaker" not in words[0]:
        return alt.get("transcript", "").strip() or "(empty transcript)"

    lines, cur_speaker, buf = [], None, []
    for w in words:
        spk = w.get("speaker", 0)
        if spk != cur_speaker:
            if buf:
                lines.append(f"[Speaker {cur_speaker}] " + " ".join(buf))
            cur_speaker, buf = spk, []
        buf.append(w.get("punctuated_word", w.get("word", "")))
    if buf:
        lines.append(f"[Speaker {cur_speaker}] " + " ".join(buf))
    return "\n\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--lang", default="ko", help="language code (ko, en, es, …)")
    ap.add_argument("--model", default="nova-2")
    ap.add_argument("--no-diarize", dest="diarize", action="store_false")
    args = ap.parse_args()

    path = Path(args.path).expanduser()
    if not path.is_file():
        sys.exit(f"File not found: {path}")

    text = transcribe(path, args.lang, args.model, args.diarize)
    out = path.with_suffix(path.suffix + ".txt")
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n[saved] {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
