---
name: stt
description: |
  Transcribe an audio file to text (speech-to-text). Use when the user types "stt" or
  attaches an audio file (mp3, m4a, wav, flac, aac, ogg, opus, webm, mp4) and asks to
  "transcribe", "turn this into text", "write this up", or "pull the audio". Uses Deepgram
  (nova-2) with speaker diarization on by default. Pairs with the `add` skill to file the
  result.
---

# stt — speech to text

Transcribes audio with Deepgram, speaker-labelled, and saves a `.txt` next to the source.

## Setup (once)

Needs a [Deepgram](https://deepgram.com) API key (generous free tier). Put it in your
environment — never in a file the agent might commit:

```bash
echo 'export DEEPGRAM_API_KEY="your-key"' >> ~/.zshrc && source ~/.zshrc
```

`pip install requests` if you don't have it.

## Step 1 — get the file path

If none was given: *"What's the path to the audio file?"* Handle multiple files in turn.

Supported: `.mp3 .m4a .wav .flac .aac .mp4 .ogg .webm .opus`

## Step 2 — language

Default **Korean (`ko`)** unless the filename/context says otherwise (change the default
in your fork). If unclear, ask briefly.

## Step 3 — run

```bash
python3 ~/.claude/skills/stt/transcribe.py "<path>" --lang <code>
```

Options: `--lang en` (or `ko`, `es`, …) · `--no-diarize` (single speaker, faster) ·
`--model nova-2`.

Quote paths that contain spaces.

## Step 4 — output

Print the transcript to the conversation. It's also saved as `<path>.txt`.

## Step 5 — file it (optional)

If the audio was notes/a meeting/a memo worth keeping, hand the transcript to the `add`
skill to route it into the workspace. Remember `add`'s rule: cross-check transcribed
names against `people.md` — STT mangles proper nouns.
