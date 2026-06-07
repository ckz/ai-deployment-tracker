"""Static source definitions for the MVP tracker."""

from __future__ import annotations

COMPANY_SOURCES = {
    "Modal": [
        {"type": "homepage", "url": "https://modal.com"},
        {"type": "docs", "url": "https://modal.com/docs"},
        {"type": "pricing", "url": "https://modal.com/pricing"},
    ],
    "Baseten": [
        {"type": "homepage", "url": "https://www.baseten.co"},
        {"type": "docs", "url": "https://docs.baseten.co"},
        {"type": "pricing", "url": "https://www.baseten.co/pricing"},
    ],
    "Railway": [
        {"type": "homepage", "url": "https://railway.app"},
        {"type": "docs", "url": "https://docs.railway.app"},
        {"type": "pricing", "url": "https://railway.app/pricing"},
    ],
    "Fal.ai": [
        {"type": "homepage", "url": "https://fal.ai"},
        {"type": "docs", "url": "https://fal.ai/docs"},
        {"type": "pricing", "url": "https://fal.ai/pricing"},
    ],
    "RunPod": [
        {"type": "homepage", "url": "https://www.runpod.io"},
        {"type": "docs", "url": "https://docs.runpod.io"},
        {"type": "pricing", "url": "https://www.runpod.io/pricing"},
    ],
    "Fireworks AI": [
        {"type": "homepage", "url": "https://fireworks.ai"},
        {"type": "docs", "url": "https://docs.fireworks.ai"},
        {"type": "pricing", "url": "https://fireworks.ai/pricing"},
    ],
    "Together AI": [
        {"type": "homepage", "url": "https://www.together.ai"},
        {"type": "docs", "url": "https://docs.together.ai"},
        {"type": "pricing", "url": "https://www.together.ai/pricing"},
    ],
    "Northflank": [
        {"type": "homepage", "url": "https://northflank.com"},
        {"type": "docs", "url": "https://northflank.com/docs"},
        {"type": "pricing", "url": "https://northflank.com/pricing"},
    ],
    "Coolify": [
        {"type": "homepage", "url": "https://coolify.io"},
        {"type": "docs", "url": "https://coolify.io/docs"},
        {"type": "pricing", "url": "https://coolify.io/pricing"},
    ],
    "Replicate": [
        {"type": "homepage", "url": "https://replicate.com"},
        {"type": "docs", "url": "https://replicate.com/docs"},
        {"type": "pricing", "url": "https://replicate.com/pricing"},
    ],
}


def get_company_sources(company_name: str) -> list[dict[str, str]]:
    return COMPANY_SOURCES.get(company_name, [])
