# 10_WORK — active projects (with deadlines)

> Things you're actively working on that have an end. When a project has no deadline,
> it's a role → `20_DOMAINS/`. When it's done → `80_ARCHIVE/`.
>
> 마감이 있는, 진행 중인 작업. 마감 없으면 역할 → `20_DOMAINS/`. 끝나면 → `80_ARCHIVE/`.

## Current projects

| Folder | Deadline | status |
|---|---|---|
| _PROJECT_TEMPLATE/ | — | (template — copy me) |

## Standard project structure

Copy `_PROJECT_TEMPLATE/` for each new project:

```
PROJECT/
├── README.md      # first line: status: <tag>; overview, deadline, who
├── docs/          # plans, proposals
├── decisions/     # decisions specific to this project
├── references/    # source material
└── outputs/       # deliverables
```

## Rules

- Every project `README.md` starts with a `status:` line.
- Done → set `status: complete`, move the folder to `80_ARCHIVE/`.
- Rejected/dead → `status: abandoned`, reason → `00_SELF/decisions/feedback_patterns.md`.
- Deadlines that matter also belong on your calendar and/or `00_SELF/memory/todo.md`.

## The stale-project sweep (do this monthly)

Projects fade out silently — a submission goes unanswered, a client goes quiet, a plan
just stops. Two rules learned the hard way:

- **Folder timestamps don't prove activity.** Real work often happens outside this
  workspace (a studio, a meeting, another tool). Never judge a project dead by mtime.
- **Never auto-archive on staleness alone.** List projects with no updates for 2–3
  months, **ask the owner** one line per project, then tag `on-hold` / `abandoned` /
  `complete` accordingly. An honest "active" table is what makes this folder trustworthy
  — a router that points at dead projects misleads every future session.
