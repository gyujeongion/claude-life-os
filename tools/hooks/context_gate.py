#!/usr/bin/env python3
"""UserPromptSubmit hook — personal-context gate (enforcement for the answer gate).

Why this exists: the workspace asks the agent to pass 00_SELF/context_router.md before
every answer, but prose rules get diluted as sessions grow long. This hook makes the one
critical rule physical: when a personal-context keyword appears in your prompt, it
injects a reminder that the public-persona layer (L1) must be OFF.

Wiring: docs/SETUP.md, step 4b. Customize KEYWORDS to your life and language — these are
English defaults. False positives are fine: the reminder itself tells the agent to ignore
it when the context is actually work/business/code.
"""

import json
import re
import sys

KEYWORDS = re.compile(
    r"""(?ix)\b(
    wedding|marriage|honeymoon|proposal|birthday|anniversary|funeral|newborn|
    invest(ing|ment)?|stocks?|portfolio|crypto|bitcoin|etf|retirement|pension|salary|budget|
    friend(ship)?|family|girlfriend|boyfriend|partner|conflict|apology|grief|
    health|diet|doctor|therapy|workout|
    shopping|fashion|outfit|vacation|home|moving|interior
    )\b""",
)
# Non-English example — if you write to your agent in another language, REPLACE the
# pattern above with keywords in that language (note: \b word boundaries don't work
# well for CJK — drop the \b wrappers like this Korean example):
# KEYWORDS = re.compile(r"(?ix)(결혼|웨딩|신혼|생일|기념일|장례|투자|주식|코인|연금|"
#                       r"친구|가족|연인|갈등|사과|건강|식단|병원|운동|쇼핑|패션|이사|여행)")

REMINDER = """[context gate — auto reminder]
A personal-context keyword was detected (class C taste / D life event / E finance / F relationships).
First confirm the context really is personal — if this is actually about the owner's public
work, business, or code (class A/B/G), ignore this reminder. If it IS personal:
1. Public-persona / brand layer (L1) is OFF. Brand strategy does not steer private life.
2. Personal-taste layer stays ON — no bland "safe default" answers.
3. Finance -> apply the owner's documented thesis, not generic risk platitudes.
4. Relationships -> check 00_SELF/people/people.md before advising.
Details: 00_SELF/context_router.md"""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = data.get("prompt") or data.get("user_prompt") or ""
    if len(prompt) < 8 or not KEYWORDS.search(prompt):
        return
    print(json.dumps(
        {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                "additionalContext": REMINDER}},
        ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # a broken hook must never block the conversation
