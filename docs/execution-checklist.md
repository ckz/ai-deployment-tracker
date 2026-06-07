# AI Deployment Platform Tracker — Execution Checklist

This file is the **step-by-step build order** for the project. Follow it in order and do not skip ahead.

## Rules

- Finish one step before starting the next.
- Keep the MVP small.
- Commit after each completed task.
- If a task grows beyond 5 minutes, split it.
- Do not add advanced features before the MVP runs end-to-end.

---

## Stage 0 — Repo foundation

### 0.1 Confirm the repo root
**Goal:** Make sure all work happens inside `~/ai_projects/ai-deployment-tracker`.

**Check:**
- `pwd` should point to the repo root
- `git status` should work

**Done when:** you know the exact repo root and branch.

---

### 0.2 Add project metadata
**Goal:** Make the repo recognizable and runnable.

**Files:**
- `pyproject.toml`
- `README.md`
- `src/tracker.py`

**Do this first:**
1. Add a minimal `pyproject.toml`.
2. Keep dependencies empty unless needed.
3. Make `src/tracker.py` callable as a CLI script.
4. Update `README.md` with run instructions.

**Done when:** `python src/tracker.py` runs successfully.

---

### 0.3 Decide the local data layout
**Goal:** Establish folders before code depends on them.

**Folders:**
- `data/companies.json`
- `data/raw/`
- `reports/daily/`
- `reports/weekly/`
- `reports/monthly/`

**Done when:** the folder layout is known and consistent.

---

## Stage 1 — Company registry

### 1.1 Create the watchlist file
**Goal:** Store the first 10 companies in a machine-readable format.

**File:** `data/companies.json`

**Include fields:**
- `name`
- `category`
- `website`
- `priority_score`
- `notes`

**Done when:** the file contains all 10 MVP companies.

---

### 1.2 Add a registry loader
**Goal:** Read the watchlist reliably from code.

**File:** `src/company_registry.py`

**Responsibilities:**
- open `data/companies.json`
- validate required fields
- return normalized records

**Done when:** the loader returns 10 structured company records.

---

### 1.3 Wire the registry into the tracker
**Goal:** Make the tracker use the company list.

**File:** `src/tracker.py`

**Behavior:**
- load watchlist
- print the number of companies loaded
- exit cleanly

**Done when:** the tracker reports the correct watchlist count.

---

## Stage 2 — Schema and evidence model

### 2.1 Define the schema
**Goal:** Create the minimal data model for the MVP.

**File:** `src/schema.sql`

**Tables:**
- `companies`
- `daily_snapshots`
- `evidence`
- `weekly_reports`

**Done when:** the schema describes every record type the MVP needs.

---

### 2.2 Add Python data structures
**Goal:** Make the schema easy to use from code.

**File:** `src/models.py`

**Approach:**
- use simple dataclasses or dictionaries
- keep it small and explicit

**Done when:** the data structures match the schema fields.

---

### 2.3 Add tests for the model layer
**Goal:** Prevent schema drift.

**File:** `tests/test_models.py`

**Done when:** tests verify the required fields are present.

---

## Stage 3 — Evidence collection

### 3.1 Define source URLs
**Goal:** Build the list of sources per company.

**File:** `src/sources.py`

**Start with:**
- homepage
- docs
- pricing
- blog
- changelog if available

**Done when:** every company has at least one source URL.

---

### 3.2 Build a fetch helper
**Goal:** Download page content consistently.

**File:** `src/collectors.py`

**Responsibilities:**
- fetch a page
- extract readable text
- return normalized content

**Done when:** the helper can fetch one page and return text.

---

### 3.3 Save raw snapshots
**Goal:** Preserve source history.

**Folder convention:**
- `data/raw/<company>/<YYYY-MM-DD>/<source>.txt`

**Done when:** fetched pages are stored as dated raw text files.

---

### 3.4 Add collector tests
**Goal:** Keep the collector stable.

**File:** `tests/test_collectors.py`

**Done when:** network is mocked and output naming is verified.

---

### 3.5 Add deduplication
**Goal:** Avoid storing the same evidence repeatedly.

**File:** `src/dedupe.py`

**Suggested key:**
- normalized URL
- content hash

**Done when:** unchanged content is skipped and changed content is stored.

---

### 3.6 Add dedupe tests
**File:** `tests/test_dedupe.py`

**Done when:** duplicate and changed-content behavior is covered.

---

## Stage 4 — Scoring and snapshots

### 4.1 Define the score inputs
**Goal:** Decide what changes a company’s momentum score.

**File:** `src/scoring.py`

**Inputs:**
- product velocity
- developer adoption
- customer proof
- pricing movement
- funding/news

**Done when:** the score inputs are clear and minimal.

---

### 4.2 Implement scoring
**Goal:** Convert signals into a 0–100 score.

**Done when:** the scorer returns a stable score for a given set of inputs.

---

### 4.3 Add scoring tests
**File:** `tests/test_scoring.py`

**Done when:** the score behaves predictably for known inputs.

---

### 4.4 Store daily snapshots
**Goal:** Save the score and summary for each company every day.

**File:** `src/storage.py`

**Done when:** a snapshot can be written and later read back.

---

### 4.5 Add snapshot tests
**File:** `tests/test_storage.py`

**Done when:** snapshot insert/retrieve behavior is tested.

---

## Stage 5 — Reports

### 5.1 Generate the daily report
**Goal:** Produce a human-readable daily summary.

**File:** `src/reports/daily.py`

**Report sections:**
- headline changes
- new evidence
- score movement
- top winners
- top losers

**Done when:** the report is valid Markdown and easy to scan.

---

### 5.2 Add daily report tests
**File:** `tests/test_daily_report.py`

**Done when:** the report includes the expected sections.

---

### 5.3 Generate weekly report
**File:** `src/reports/weekly.py`

**Done when:** it summarizes score movement over the week.

---

### 5.4 Generate monthly report
**File:** `src/reports/monthly.py`

**Done when:** it summarizes longer-term momentum trends.

---

### 5.5 Add report tests
**File:** `tests/test_reports.py`

**Done when:** weekly/monthly outputs are validated.

---

## Stage 6 — Automation and publishing

### 6.1 Add daily automation
**File:** `.github/workflows/daily.yml`

**Goal:** Run the tracker on a schedule.

**Done when:** the workflow is syntactically valid.

---

### 6.2 Add GitHub Pages deployment
**File:** `.github/workflows/pages.yml`

**Goal:** Publish weekly/monthly reports via GitHub Pages.

**Done when:** report output can be published automatically.

---

## Stage 7 — Iteration later

### 7.1 Add more source coverage
**Goal:** Expand beyond homepages.

**Possible sources:**
- docs
- changelogs
- pricing
- release notes
- blogs
- social/search signals

---

### 7.2 Move storage to Postgres when needed
**Goal:** Keep the schema but swap the backend.

---

### 7.3 Add vector search later
**Goal:** Enable semantic search over evidence and reports.

---

## MVP completion checklist

The MVP is done when:

- the tracker runs end to end
- the watchlist loads correctly
- evidence is collected and deduplicated
- daily snapshots are stored
- scores move over time
- daily reports are generated
- weekly/monthly reports can be published to GitHub Pages

---

## Suggested build order

1. `pyproject.toml`
2. `src/tracker.py` CLI
3. `data/companies.json`
4. `src/company_registry.py`
5. `src/schema.sql`
6. `src/models.py`
7. `src/sources.py`
8. `src/collectors.py`
9. `src/dedupe.py`
10. `src/scoring.py`
11. `src/storage.py`
12. `src/reports/daily.py`
13. `src/reports/weekly.py`
14. `src/reports/monthly.py`
15. GitHub Actions workflows

