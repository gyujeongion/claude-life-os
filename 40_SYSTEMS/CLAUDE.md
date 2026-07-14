# 40_SYSTEMS — code, automation, infrastructure

> The tools you've built and the automation that runs your life. Scripts, collectors,
> hooks, servers. This is the one ring that *is* developer-ish — but you only touch it if
> you want to automate. The workspace works fully without anything here.
>
> 당신이 만든 도구와 라이프 OS를 돌리는 자동화. 스크립트·수집기·훅·서버. 이 링만 개발
> 성격이지만, 자동화하고 싶을 때만 손대면 됩니다. 여기 아무것도 없어도 워크스페이스는
> 완전히 작동합니다.

## Suggested layout

```
40_SYSTEMS/
├── scripts/      # one-off and utility scripts
├── automation/   # scheduled jobs, hooks, always-on services
└── data/         # local data stores the systems read/write
```

## Rules

- **Secrets go in `.env`, never in code or `.md`.** (`.env` is gitignored.)
- Note where each thing runs (this machine? a server? a schedule?).
- Always-on automation should say how it's kept alive (a launchd/systemd/cron entry).
- Prefer structured, modular code over one-off glue. Future-you maintains this.

## Data placement

| Data kind | Where |
|---|---|
| I/O-heavy, frequent writes | fast local disk |
| large, archival, infrequent | bulk/network storage |
