# 00_SELF — the center

> This is who you are. The agent reads this hub, then opens only the one file it needs.
> 여기가 중심입니다. 에이전트는 이 허브를 읽고 필요한 파일 하나만 엽니다.

## Session entry order

1. `memory/agent_brain/MEMORY.md` — core facts about the owner + environment
2. `memory/agent_brain/USER.md` — how the owner likes to communicate
3. `memory/shared_memory.md` — recent cross-session context
4. (on demand) the specific file the request calls for, from the tables below

## Subfolders

| Folder | Holds | Key file |
|---|---|---|
| `identity/` | who the owner is + patterns the agent notices | `character.md` |
| `decisions/` | confirmed decisions + rejection filters | `decisions_log.md` |
| `people/` | everyone the agent should recognize | `people.md` |
| `memory/` | global / project / session memory | `MEMORY_RULES.md` |
| — | the answer gate | `context_router.md` |

## `identity/` — when to read what

| File | Contents | Read when |
|---|---|---|
| `character.md` | owner's personality, thinking, taste `[OWNER]` | any taste / judgment / proposal call |
| `character_ai_mirror.md` | patterns the agent has observed `[AI]` | reasoning about the owner's tendencies |

## `decisions/` — when to read what

| File | Contents | Read when |
|---|---|---|
| `decisions_log.md` | confirmed decisions `[OWNER]` | before proposing anything strategic |
| `feedback_patterns.md` | rejected patterns + rules `[OWNER]` | before proposing anything at all |

## Source discipline

- `[OWNER]` = the owner said it. Lives in `decisions/`. Highest authority.
- `[AI]` = the agent inferred it. Lives in `character_ai_mirror.md` / `30_KNOWLEDGE/`.
- On conflict, `[OWNER]` wins.

## The answer gate

Before generating any answer, pass `context_router.md`. It decides which principle
layers apply to *this* request. This is not optional — it's what keeps the agent from
answering a personal question with a work rulebook.
