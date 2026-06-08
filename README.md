# AI Deployment Platform Tracker

Continuous market intelligence for AI deployment, inference, and developer platforms.

## What this repo is

- `docs/v1-design.md` — the full original design
- `docs/mvp-plan.md` — the simplified MVP for fast iteration
- `docs/implementation-plan-v1.md` — the implementation plan
- `docs/execution-checklist.md` — the step-by-step build checklist
- `src/` — implementation code
- `data/` — local watchlist and runtime state
- `reports/daily/` — generated daily reports

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

## Hermes cron automation

The repo now includes:

- `docs/research-rubric.md` — shared scoring, dedupe, and sector-selection rubric
- `~/.hermes/scripts/ai-deployment-tracker-daily.sh` — daily helper that runs the tracker and pushes report updates
- `.github/workflows/pages.yml` — GitHub Pages deployment for the generated `reports/` folder

The Hermes cron setup now runs three jobs:
- daily tracker briefing
- daily adjacent-sector discovery
- weekly summary that merges both daily streams and dedupes overlap

The daily helper will:
- source `~/.hermes/.env` if present
- run the tracker
- commit any new `reports/` output
- push to `origin/main`

GitHub Actions then deploys the generated `reports/` folder to GitHub Pages.
