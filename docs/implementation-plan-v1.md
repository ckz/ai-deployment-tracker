# AI Deployment Platform Tracker — Implementation Plan v1

> **For Hermes:** Use the plan task-by-task. Keep the MVP small and iterate from there.

**Goal:** Build a daily market-intelligence tracker that monitors a small set of AI deployment/platform companies, stores evidence, scores movement, and publishes weekly/monthly reports to GitHub Pages.

**Architecture:** Start with a lightweight Python MVP using local files plus SQLite. Collect daily evidence from official sources, normalize it into a small schema, compute a simple momentum score, and render Markdown reports. Keep the design open so we can later swap SQLite for Postgres/pgvector and add richer search and dashboards.

**Tech Stack:** Python 3, SQLite, Markdown, GitHub Actions, GitHub Pages, standard library + a few small parsing libraries later.

---

## Phase 0 — Repository foundation

### Task 1: Add a project manifest and keep the repo easy to run
**Objective:** Make the project runnable with a minimal Python entrypoint and a clear dependency story.

**Files:**
- Create: `pyproject.toml`
- Modify: `README.md`
- Modify: `src/tracker.py`

**Step 1: Create the manifest**
- Add project metadata and a `tracker` console entrypoint later if needed.
- Start dependency-free unless we truly need packages.

**Step 2: Update the README**
- Document how to run the tracker locally.
- Explain where reports live and how GitHub Pages fits in.

**Step 3: Replace the print-only script**
- Turn `src/tracker.py` into a small CLI wrapper that can:
  - load the company list
  - write a stub daily report
  - exit cleanly

**Step 4: Verify**
- Run `python src/tracker.py`
- Expected: the script runs without error and prints a useful message.

**Step 5: Commit**
- Commit message: `chore: add project manifest and tracker entrypoint`

---

### Task 2: Create the initial company registry
**Objective:** Store the first watchlist in a simple machine-readable file.

**Files:**
- Create: `data/companies.json`
- Create: `src/company_registry.py`
- Modify: `src/tracker.py`

**Step 1: Write the registry file**
- Include the 10 MVP companies.
- Add fields: `name`, `category`, `website`, `priority_score`, `notes`.

**Step 2: Add a loader**
- Create a helper that reads `data/companies.json` and returns normalized records.

**Step 3: Wire it into the tracker**
- Make `src/tracker.py` load and print the active watchlist count.

**Step 4: Verify**
- Run `python src/tracker.py`
- Expected: it reports 10 companies loaded.

**Step 5: Commit**
- Commit message: `feat: add initial company registry`

---

## Phase 1 — Evidence collection

### Task 3: Define the evidence model
**Objective:** Establish the smallest useful schema for daily market observations.

**Files:**
- Create: `src/models.py`
- Create: `src/schema.sql`
- Create: `tests/test_models.py`

**Step 1: Define the schema**
- `companies`
- `daily_snapshots`
- `evidence`
- `weekly_reports`

**Step 2: Define Python data shapes**
- Keep them simple: dicts or dataclasses.

**Step 3: Add tests**
- Verify the schema has the required columns/fields.

**Step 4: Verify**
- Run the model tests.
- Expected: schema/shape tests pass.

**Step 5: Commit**
- Commit message: `feat: define evidence and snapshot schema`

---

### Task 4: Build the first evidence collector
**Objective:** Pull a small set of official pages for each company and save raw text.

**Files:**
- Create: `src/collectors.py`
- Create: `src/sources.py`
- Create: `data/raw/` (directory convention)
- Create: `tests/test_collectors.py`

**Step 1: Add the source map**
- Store official source URLs per company.
- Start with docs/blog/pricing/homepage only.

**Step 2: Build a fetch helper**
- Fetch the page content and return plain text.

**Step 3: Save raw snapshots**
- Write raw content into a dated file path.

**Step 4: Add tests**
- Mock the network and verify text extraction + file naming.

**Step 5: Verify**
- Run collector tests.
- Expected: it stores one snapshot per source.

**Step 6: Commit**
- Commit message: `feat: add basic evidence collector`

---

### Task 5: Deduplicate evidence entries
**Objective:** Avoid storing the same evidence every day.

**Files:**
- Create: `src/dedupe.py`
- Modify: `src/collectors.py`
- Create: `tests/test_dedupe.py`

**Step 1: Decide a dedupe key**
- Example: normalized URL + content hash.

**Step 2: Implement dedupe logic**
- Skip inserts for duplicates.

**Step 3: Add tests**
- Same content should be rejected.
- Changed content should be accepted.

**Step 4: Verify**
- Run dedupe tests.

**Step 5: Commit**
- Commit message: `feat: deduplicate daily evidence`

---

## Phase 2 — Scoring and snapshots

### Task 6: Add a simple scoring function
**Objective:** Convert daily evidence into a 0–100 momentum score.

**Files:**
- Create: `src/scoring.py`
- Create: `tests/test_scoring.py`

**Step 1: Define the score inputs**
- product velocity
- adoption
- customer proof
- pricing movement
- funding/news

**Step 2: Implement the scoring function**
- Start with a weighted sum.

**Step 3: Add tests**
- Verify known inputs map to expected scores.
- Verify score changes when a strong signal arrives.

**Step 4: Verify**
- Run scoring tests.

**Step 5: Commit**
- Commit message: `feat: add simple momentum scoring`

---

### Task 7: Record daily snapshots
**Objective:** Save the company score and a short summary once per day.

**Files:**
- Create: `src/storage.py`
- Modify: `src/tracker.py`
- Create: `tests/test_storage.py`

**Step 1: Write snapshot helpers**
- Insert one daily row per company.

**Step 2: Store summary text**
- Keep a one-paragraph explanation of why the score changed.

**Step 3: Add tests**
- Verify a snapshot is written and retrievable.

**Step 4: Verify**
- Run storage tests.

**Step 5: Commit**
- Commit message: `feat: store daily snapshots`

---

## Phase 3 — Reports

### Task 8: Generate a daily Markdown report
**Objective:** Produce a readable daily summary from the latest snapshot data.

**Files:**
- Create: `src/reports/daily.py`
- Create: `reports/daily/` output convention
- Create: `tests/test_daily_report.py`

**Step 1: Define report structure**
- headline changes
- new evidence
- score movement
- top winners/losers

**Step 2: Render Markdown**
- Keep it simple and readable.

**Step 3: Add tests**
- Verify key sections appear in the output.

**Step 4: Verify**
- Run daily report tests.

**Step 5: Commit**
- Commit message: `feat: generate daily markdown report`

---

### Task 9: Generate weekly and monthly reports
**Objective:** Summarize momentum trends over longer windows.

**Files:**
- Create: `src/reports/weekly.py`
- Create: `src/reports/monthly.py`
- Create: `tests/test_reports.py`

**Step 1: Define weekly/monthly sections**
- top risers
- top decliners
- category trends
- new entrants
- recommended follow-up

**Step 2: Render Markdown files**
- Output to a GitHub Pages-friendly directory.

**Step 3: Add tests**
- Verify the reports include the expected headings and data.

**Step 4: Verify**
- Run report tests.

**Step 5: Commit**
- Commit message: `feat: add weekly and monthly reports`

---

## Phase 4 — Automation

### Task 10: Add GitHub Actions scheduling
**Objective:** Run the tracker automatically every day.

**Files:**
- Create: `.github/workflows/daily.yml`
- Create: `.github/workflows/pages.yml`

**Step 1: Add daily schedule workflow**
- Run the tracker on a cron schedule.

**Step 2: Add Pages deployment workflow**
- Publish report output from the repository.

**Step 3: Verify YAML validity**
- Ensure workflows are syntactically valid.

**Step 4: Commit**
- Commit message: `chore: add github actions automation`

---

## Phase 5 — Iteration and expansion

### Task 11: Add better source coverage
**Objective:** Expand the evidence sources beyond company homepages.

**Files:**
- Modify: `src/sources.py`
- Modify: `src/collectors.py`

**Target sources:**
- docs
- changelogs
- pricing
- release notes
- blog posts
- social/search signals

---

### Task 12: Move from SQLite to Postgres when needed
**Objective:** Upgrade storage without rewriting the project.

**Files:**
- Modify: `src/storage.py`
- Modify: `src/schema.sql`
- Add: migration scripts if necessary

---

### Task 13: Add vector search later
**Objective:** Support semantic queries across evidence and reports.

**Files:**
- Create: `src/vector_store.py`
- Modify: `src/storage.py`

---

## Suggested execution order

1. project manifest
2. company registry
3. schema
4. evidence collector
5. deduplication
6. scoring
7. daily snapshots
8. daily report
9. weekly/monthly reports
10. GitHub Actions automation
11. later improvements

## Definition of done for MVP

- daily run completes successfully
- evidence is stored consistently
- scores update over time
- reports are generated automatically
- weekly/monthly reports can be published to GitHub Pages
