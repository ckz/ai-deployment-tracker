# AI Deployment Platform Tracker — v1 Design

**Goal**: Track which AI deployment/platform companies are gaining momentum over days, weeks, and months.

## 1. Companies to Track First

Start with these groups:

- **Edge AI app platforms**: Cloudflare, Vercel, Netlify
- **Developer clouds**: Railway, Render, Fly.io, DigitalOcean, Northflank
- **AI/GPU platforms**: Modal, Baseten, Replicate, RunPod, Fal.ai, Together AI, Fireworks AI
- **Self-hosted PaaS**: Coolify, Dokploy
- **AI workflow/productivity**: Notion, Airtable, Zapier, Make

Cloudflare and Vercel are especially important because both now offer AI Gateway-style routing, observability, caching, fallback, and model access features.

## 2. Data to Collect Daily

For each company, collect:

- Product launches
- Pricing changes
- Funding/news
- Developer adoption
- Customer proof
- Technical quality
- Hiring
- Search/social trend

## 3. Database Design

Use three layers:

### A. Structured database
Use Postgres.

Core tables:
- `companies`
- `daily_snapshots`
- `evidence`
- `weekly_reports`

### B. Vector knowledge base
Use pgvector, Supabase Vector, Weaviate, Pinecone, or Cloudflare Vectorize.

Store embeddings for:
- news articles
- docs pages
- pricing pages
- blog posts
- release notes
- case studies
- social discussions
- previous reports

### C. Raw archive
Keep raw HTML/text in object storage.

## 4. Daily Cron Workflow

1. Pull source list
2. Search web/news/product pages for each company
3. Scrape official docs, changelog, pricing, blog
4. Pull GitHub/reddit/HN/social signals where available
5. Deduplicate against yesterday’s findings
6. Embed all new evidence into vector DB
7. Score each company
8. Generate daily delta report
9. Store report and update dashboard

## 5. Scoring Model

Score each company from 0–100.

| Factor | Weight |
|--------|--------|
| Product velocity | 25 |
| AI-native fit | 20 |
| Developer adoption | 20 |
| Revenue/enterprise signal | 15 |
| Funding/partnerships | 10 |
| Differentiation | 10 |

The key is not just score; track **score movement** over time.

## 6. Reports to Generate

- **Daily report**: today’s notable changes
- **Weekly report**: rising/declining companies + trends
- **Monthly report**: traction vs hype, acquisition targets, category heat

## 7. Recommended Stack

For a lean first version:

- **Cron**: GitHub Actions
- **Backend**: Python
- **Database**: Postgres + pgvector (or SQLite first)
- **Search**: Web/news APIs
- **Embeddings**: OpenAI / Voyage / Jina
- **Dashboard**: simple Next.js or static pages
- **Reports**: Markdown + GitHub Pages
- **Storage**: S3/R2
