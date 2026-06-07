# AI Deployment Platform Tracker — MVP Plan (Simplified)

**Objective**: Build the smallest possible version that delivers daily intelligence and is easy to iterate on later.

## MVP Scope

Track only 10 core companies first:

- Modal
- Baseten
- Railway
- Fal.ai
- RunPod
- Fireworks AI
- Together AI
- Northflank
- Coolify
- Replicate

Collect evidence from:
- official blogs
- docs
- pricing pages
- changelogs
- news

## MVP Output

- daily evidence collection
- simple score per company
- daily markdown report
- weekly markdown report
- publish reports via GitHub Pages

## 4-Week Plan

1. **Week 1**: basic data collection script
2. **Week 2**: scoring + local storage
3. **Week 3**: reports + GitHub Pages
4. **Week 4**: automation + cleanup

## Tech Decisions

- **Language**: Python
- **Database**: SQLite first, Postgres later
- **Reports**: Markdown files
- **Cron**: GitHub Actions

## Success Criteria

- runs daily without manual work
- score movement is visible over time
- easy to add more companies later
