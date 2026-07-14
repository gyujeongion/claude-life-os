<h1 align="center">🌀 Life Agent for Claude Code</h1>

<p align="center">
  <b>Turn your Claude Code into a personal agent that actually knows your life.</b><br>
  A folder architecture that organizes <i>you</i> — not your codebase — as concentric circles,<br>
  so the AI navigates your life the way you would.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="docs/ARCHITECTURE.md">Architecture</a> ·
  <a href="docs/CONVENTIONS.md">Conventions</a> ·
  <a href="#한국어">한국어</a>
</p>

---

## What this is

Most AI-agent templates are built for **developers** — they organize a codebase.
This one is built for **a person**. It's a workspace where an AI agent holds your
identity, your decisions, the people in your life, your ongoing projects, your money,
your health — and knows *when* to look at each, and *which rules apply* to each.

You point Claude Code at this folder. From then on it stops being a generic assistant
and starts being **your** agent: it remembers what you decided, filters proposals
through your taste, and never gives you career advice using the rules meant for your
relationships.

**No coding experience required.** If you can fill in a form, you can adopt this.

> **Private by default.** Your personal files (identity, people, decisions, memory) are
> git-ignored from the start — the template ships them as `*.example` seeds and
> `bootstrap.sh` creates your live copies locally. So your life is never committed or
> published, even if your copy is public. Framework files stay tracked, so you can still
> pull improvements ([UPDATE.md](UPDATE.md)).

## The mental model: your life as concentric circles

```
                    ┌─────────────────────────────┐
                    │        80_ARCHIVE           │   done / inactive
                    │  ┌───────────────────────┐  │
                    │  │      50_LIFE          │  │   money · family · health
                    │  │  ┌─────────────────┐  │  │
                    │  │  │   40_SYSTEMS    │  │  │   code · automation
                    │  │  │ ┌─────────────┐ │  │  │
                    │  │  │ │30_KNOWLEDGE │ │  │  │   research · knowledge
                    │  │  │ │┌───────────┐│ │  │  │
                    │  │  │ ││20_DOMAINS ││ │  │  │   ongoing roles
                    │  │  │ ││┌─────────┐││ │  │  │
                    │  │  │ │││ 10_WORK │││ │  │  │   active projects
                    │  │  │ │││┌───────┐│││ │  │  │
                    │  │  │ ││││00_SELF││││ │  │  │   ← YOU (center)
                    │  │  │ │││└───────┘│││ │  │  │
                    │  │  │ ││└─────────┘││ │  │  │
                    │  │  │ │└───────────┘│ │  │  │
                    │  │  │ └─────────────┘ │  │  │
                    │  │  └─────────────────┘  │  │
                    │  └───────────────────────┘  │
                    └─────────────────────────────┘
                                                        90_SHARED — an isolated
                                                        second agent (e.g. a shared
                                                        family/partner assistant)
```

The closer to the center, the more it *is* you. The agent starts from `00_SELF`
and only moves outward as far as the request requires.

## Why it works: two gates

Every request passes through two decision points:

1. **Navigation gate** (`CLAUDE.md` in each folder) — *which files do I open?*
   The agent follows a mapping table down the folder tree instead of scanning everything.
2. **Answer gate** (`00_SELF/context_router.md`) — *which of my principles apply?*
   Advice about your investments should not run on the same rules as advice about a
   friendship. The router classifies the request and switches principle-layers on/off.

This is the core insight most personal-agent setups miss: **context determines not just
what the AI reads, but which version of "you" it answers as.**

## What's inside

| Ring | Folder | Holds |
|---|---|---|
| Center | `00_SELF/` | identity, memory, decisions, the people in your life, the answer-gate router |
| 1 | `10_WORK/` | active projects **with deadlines** |
| 2 | `20_DOMAINS/` | ongoing roles with **no deadline** (a job, a side business, a craft) |
| 3 | `30_KNOWLEDGE/` | research, analysis, things you've learned |
| 4 | `40_SYSTEMS/` | code, automation, scripts, infrastructure |
| 5 | `50_LIFE/` | money, family, health, admin |
| — | `80_ARCHIVE/` | finished and inactive things |
| — | `90_SHARED/` | an **isolated** second agent — e.g. a companion assistant you share with a partner, sandboxed away from everything above |

Inside `00_SELF` you'll find the engine:
- **`identity/character.md`** — who you are (the agent reads this before making taste calls)
- **`identity/character_ai_mirror.md`** — where the agent logs patterns it notices in you
- **`decisions/decisions_log.md`** — what you've decided (so it never re-litigates)
- **`decisions/feedback_patterns.md`** — what you've rejected (so it stops proposing it)
- **`people/people.md`** — everyone the agent should recognize
- **`memory/`** — global + project memory with on-demand loading
- **`context_router.md`** — the answer gate

## Quick start

```bash
# 1. Get your own copy. Recommended: on GitHub click "Use this template" →
#    create a PRIVATE repository, then clone yours. (Just trying it? Clone this repo.)
git clone https://github.com/YOUR-USERNAME/my-workspace.git my-workspace
cd my-workspace

# 2. Open it with Claude Code
claude
```

Then paste one prompt:

> **"Read INSTALL.md and set this up for me."**

The agent bootstraps your (private, git-ignored) data files, then runs
[`ONBOARDING.md`](ONBOARDING.md) — an interview that tailors the workspace to *your* life:
it reshapes the domains and answer-gate contexts around your actual roles, not a generic
example. One question at a time, every draft shown for your OK, stop after the identity step
if you like. No coding, nothing memorized.

Prefer to do it by hand? `bash tools/bootstrap.sh`, fill `{{...}}` tokens in `CLAUDE.md`,
write 5 lines in `00_SELF/identity/character.md`, and start talking.

Full install → **[INSTALL.md](INSTALL.md)** · walkthrough → **[docs/SETUP.md](docs/SETUP.md)** · Korean → **[docs/QUICKSTART.ko.md](docs/QUICKSTART.ko.md)**

## Optional power-ups

The workspace is complete on its own. Three add-ons make it nicer to live in — all opt-in:

| Add-on | What it gives you | Setup |
|---|---|---|
| [`skills/add`](skills/add/SKILL.md) | Brain-dump anything; the agent files each piece into the right place, never overwriting. | symlink, no keys |
| [`skills/stt`](skills/stt/SKILL.md) | Transcribe a voice memo, then let `add` file it. | Deepgram key (free tier) |
| [`extras/conversation-memory`](extras/conversation-memory/) | The agent recalls relevant **past conversations** automatically — local, self-hosted. | a background service (the agent can build it with you) |

See [`skills/README.md`](skills/README.md) to install the skills.

## Design principles

- **Pointers, not piles.** Every folder's `CLAUDE.md` is a signpost, not a dump.
- **On-demand loading.** Project memory loads only when its `trigger_keywords` match.
- **Owner truth wins.** `[OWNER]` statements beat `[AI]` inferences, always.
- **Context switches the rules.** The same agent answers as different "you" depending on domain.
- **Rejections are memory.** Say no once; it won't propose that again.

---

## 한국어

### 이게 뭔가요

대부분의 AI 에이전트 템플릿은 **개발자**를 위한 것입니다 — 코드베이스를 정리하죠.
이건 **사람**을 위한 것입니다. AI 에이전트가 당신의 정체성·결정·인간관계·진행 중인
프로젝트·돈·건강을 담고, 각각을 *언제* 봐야 하는지, *어떤 원칙*을 적용해야 하는지 아는
워크스페이스입니다.

클로드 코드를 이 폴더에 연결하면, 그 순간부터 범용 비서가 아니라 **당신의** 에이전트가
됩니다. 당신이 뭘 결정했는지 기억하고, 제안을 당신의 취향으로 거르고, 인간관계에 쓰는
규칙으로 커리어 조언을 하지 않습니다.

**코딩 지식 필요 없습니다.** 양식을 채울 수 있으면 누구나 이식할 수 있습니다.

### 핵심 개념: 인생을 동심원으로

중심(`00_SELF`)에 가까울수록 그게 곧 *당신*입니다. 에이전트는 항상 중심에서 출발해,
요청이 필요로 하는 만큼만 바깥 링으로 나아갑니다.

### 왜 작동하나: 두 개의 게이트

1. **탐색 게이트** (각 폴더의 `CLAUDE.md`) — *어떤 파일을 열까?* 전부 뒤지지 않고
   매핑 테이블을 따라 폴더 트리를 내려갑니다.
2. **답변 게이트** (`00_SELF/context_router.md`) — *어떤 원칙을 적용할까?* 투자 조언과
   우정에 대한 조언은 같은 규칙으로 답하면 안 됩니다. 라우터가 요청을 분류하고 원칙
   레이어를 켜고 끕니다.

대부분의 개인 에이전트 세팅이 놓치는 핵심: **맥락은 AI가 무엇을 읽느냐뿐 아니라, 어떤
버전의 "당신"으로 답하느냐까지 결정합니다.**

### 시작하기

전체 안내 → **[docs/QUICKSTART.ko.md](docs/QUICKSTART.ko.md)**

---

<p align="center"><sub>MIT License · Built as a portable template. Fork it, fill it, make it yours.</sub></p>
