# AI Deployment Platform Tracker

Continuous market intelligence for AI deployment, inference, and developer platforms.

## What this repo is

- `docs/v1-design.md` — the full original design
- `docs/mvp-plan.md` — the simplified MVP for fast iteration
- `docs/implementation-plan-v1.md` — the implementation plan
- `docs/execution-checklist.md` — the step-by-step build checklist
- `docs/research-rubric.md` — shared scoring, dedupe, and sector-selection rubric
- `src/` — implementation code
- `data/` — local watchlist and runtime state
- `reports/daily/` — generated daily reports
- `reports/briefings/` — saved agentic briefings from the Hermes cron jobs

Weekly and monthly reports will be published via **GitHub Pages**.

## Run the MVP

From the repo root:

```bash
python src/tracker.py
```

Or use the helper wrapper:

```bash
bash scripts/run_daily_tracker.sh
```

This will:
- load the 10-company watchlist
- fetch the configured source pages
- write raw snapshots under `data/raw/`
- store state in `data/tracker.db`
- generate a daily report in `reports/daily/YYYY-MM-DD.md`
- update `reports/index.html` for GitHub Pages

## Publish saved reports

When any report or briefing files under `reports/` are ready to publish, run:

```bash
bash scripts/publish_reports.sh
```

That script stages all `reports/` artifacts, commits them, and pushes to `origin/main`.

## Hermes cron automation

The repo now includes:

- `docs/research-rubric.md` — shared scoring, dedupe, and sector-selection rubric
- `~/.hermes/scripts/ai-deployment-tracker-daily.sh` — daily helper that runs the tracker and pushes report updates
- `.github/workflows/pages.yml` — GitHub Pages deployment for the generated `reports/` folder

The Hermes cron setup now runs four jobs:

- daily tracker briefing
- daily adjacent-sector discovery
- weekly summary that merges both daily streams and dedupes overlap
- end-of-week review that checks whether the three research jobs are producing useful signal

The daily helper will:
- source `~/.hermes/.env` if present
- run the tracker
- commit any new `reports/` output
- push to `origin/main`

GitHub Actions then deploys the generated `reports/` folder to GitHub Pages.
