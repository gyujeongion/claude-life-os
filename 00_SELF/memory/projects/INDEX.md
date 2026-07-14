# projects/INDEX.md — project memory registry

> The load switch for project memory. When a message matches a project's
> `trigger_keywords`, the agent loads that project's `{slug}.md` — and nothing else.
> This is what keeps context small no matter how many projects you track.
>
> 프로젝트 메모리 로딩 스위치. 메시지가 어떤 프로젝트의 `trigger_keywords`와 매칭되면 그
> `{slug}.md`만 로드. 프로젝트가 많아도 컨텍스트가 작게 유지되는 이유.

## Active

| Slug | Project | Trigger keywords | Deadline / key date |
|---|---|---|---|
| *(illustrative row — replace with your first project)* | Example Project | example, demo, placeholder | YYYY-MM-DD |

## On-hold / Complete / Abandoned

| Slug | Project | Status | Note |
|---|---|---|---|
| — | — | — | — |

---

## How it works

```
message: "any update on the demo?"
  → keyword "demo" matches a project's trigger_keywords in the table above
  → agent loads projects/{that-slug}.md  (created from _TEMPLATE.md)
  → agent does NOT load any other project file
```

To add a project: copy `_TEMPLATE.md` → `{slug}.md`, fill the frontmatter, add a row here.
