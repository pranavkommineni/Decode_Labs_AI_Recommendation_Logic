"""
AI Career Engine — FastAPI Backend
Endpoints: /recommend · /explain · /skills · /roles · /analytics · /health
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import time

from recommendation_engine import (
    get_recommendations,
    explain_recommendation,
    compute_analytics,
    JOB_ROLES_DB,
    ALL_SKILLS,
    CATEGORIES,
)

app = FastAPI(
    title="AI Career Recommendation Engine API",
    description="Hybrid TF-IDF × BM25 × Skill-Graph recommendation engine for tech careers.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Schemas ─────────────────────────────────────────────────────────────────

class RecommendRequest(BaseModel):
    skills: list[str] = Field(..., min_items=1, max_items=50, example=["python", "machine learning", "sql"])
    top_n: int = Field(default=12, ge=1, le=80)
    diversify: bool = False
    strict: bool = False
    category: Optional[str] = None


class ExplainRequest(BaseModel):
    role_id: int
    skills: list[str]


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": time.time(), "version": "2.0.0"}


@app.get("/api/skills")
async def list_skills(q: str = Query(default="", description="Filter skills by query")):
    if q:
        filtered = [s for s in ALL_SKILLS if q.lower() in s.lower()]
    else:
        filtered = ALL_SKILLS
    return {"skills": filtered, "total": len(filtered)}


@app.get("/api/roles")
async def list_roles(
    category: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = Query(default=80, le=80),
):
    roles = JOB_ROLES_DB
    if category:
        roles = [r for r in roles if r["category"] == category]
    if q:
        q_lower = q.lower()
        roles = [r for r in roles if q_lower in r["title"].lower() or q_lower in " ".join(r["tags"])]
    return {
        "roles": roles[:limit],
        "total": len(roles),
        "categories": CATEGORIES,
    }


@app.get("/api/roles/{role_id}")
async def get_role(role_id: int):
    role = next((r for r in JOB_ROLES_DB if r["id"] == role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role {role_id} not found")
    return role


@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    if not req.skills:
        raise HTTPException(status_code=400, detail="At least one skill is required")

    result = get_recommendations(
        user_skills=req.skills,
        top_n=req.top_n,
        diversify=req.diversify,
        strict=req.strict,
        category_filter=req.category,
    )
    return result


@app.post("/api/explain")
async def explain(req: ExplainRequest):
    role = next((r for r in JOB_ROLES_DB if r["id"] == req.role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role {req.role_id} not found")

    # Run recommendation to get match scores
    rec_result = get_recommendations(req.skills, top_n=80)
    matched_role = next(
        (r for r in rec_result["recommendations"] if r["id"] == req.role_id), None
    )
    if not matched_role:
        matched_role = {**role, "matched_tags": [], "missing_tags": role["tags"][:5],
                        "match_score": 0, "coverage_pct": 0}

    return explain_recommendation(matched_role, req.skills)


@app.post("/api/analytics")
async def analytics(req: RecommendRequest):
    result = get_recommendations(
        user_skills=req.skills,
        top_n=req.top_n,
        diversify=req.diversify,
    )
    analytics_data = compute_analytics(req.skills, result["recommendations"])
    return {
        "analytics": analytics_data,
        "meta": result["meta"],
    }


@app.get("/api/categories")
async def list_categories():
    cat_counts = {}
    for role in JOB_ROLES_DB:
        cat = role["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    return {"categories": [{"name": k, "count": v} for k, v in sorted(cat_counts.items())]}


@app.get("/api/stats")
async def global_stats():
    demands = [r["demand"] for r in JOB_ROLES_DB]
    return {
        "total_roles": len(JOB_ROLES_DB),
        "total_skills": len(ALL_SKILLS),
        "total_categories": len(CATEGORIES),
        "avg_demand": round(sum(demands) / len(demands), 1),
        "remote_roles": sum(1 for r in JOB_ROLES_DB if r.get("remote")),
        "top_category": max(
            set(r["category"] for r in JOB_ROLES_DB),
            key=lambda c: sum(1 for r in JOB_ROLES_DB if r["category"] == c)
        ),
    }