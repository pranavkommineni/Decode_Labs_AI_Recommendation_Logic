"""
AI Career Recommendation Engine — Core
Algorithms: TF-IDF · Cosine Similarity · BM25 · Skill Graph · XAI
"""
from __future__ import annotations
import math
import time
from typing import Any
from data import JOB_ROLES_DB, ALL_SKILLS, CATEGORIES


# ─── TF-IDF ─────────────────────────────────────────────────────────────────

def _build_idf(roles: list[dict]) -> dict[str, float]:
    N = len(roles)
    df: dict[str, int] = {}
    for role in roles:
        for tag in set(role["tags"]):
            df[tag] = df.get(tag, 0) + 1
    return {term: math.log((N + 1) / (freq + 1)) + 1 for term, freq in df.items()}


def _tfidf_vector(tags: list[str], idf: dict[str, float]) -> dict[str, float]:
    vec: dict[str, float] = {}
    n = len(tags)
    for tag in tags:
        tf = tags.count(tag) / n
        vec[tag] = tf * idf.get(tag, math.log(len(JOB_ROLES_DB) + 1))
    return vec


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    dot = sum(a.get(k, 0) * v for k, v in b.items())
    mag_a = math.sqrt(sum(v ** 2 for v in a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ─── BM25 (bonus ranking signal) ────────────────────────────────────────────

def _bm25_score(user_skills: list[str], role_tags: list[str],
                idf: dict[str, float], k1: float = 1.5, b: float = 0.75) -> float:
    avgdl = sum(len(r["tags"]) for r in JOB_ROLES_DB) / len(JOB_ROLES_DB)
    dl = len(role_tags)
    score = 0.0
    for skill in user_skills:
        s = skill.lower()
        if s in role_tags:
            freq = role_tags.count(s)
            numerator = idf.get(s, 1.0) * freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * dl / avgdl)
            score += numerator / denominator
    return score


# ─── Skill-Graph Bonus ───────────────────────────────────────────────────────

SKILL_GRAPH: dict[str, list[str]] = {
    "machine learning": ["python", "statistics", "deep learning", "feature engineering"],
    "deep learning": ["python", "pytorch", "tensorflow", "mathematics", "gpu"],
    "react": ["javascript", "typescript", "html", "css", "nextjs"],
    "kubernetes": ["docker", "linux", "cloud", "networking", "ci/cd"],
    "aws": ["cloud", "networking", "security", "terraform", "iam"],
    "data analysis": ["python", "sql", "statistics", "visualization", "excel"],
    "nlp": ["python", "machine learning", "deep learning", "transformers", "linguistics"],
    "llm": ["python", "prompt engineering", "rag", "langchain", "huggingface"],
    "blockchain": ["solidity", "cryptography", "distributed systems", "ethereum", "web3"],
    "computer vision": ["python", "opencv", "deep learning", "pytorch", "cuda"],
}

def _skill_graph_bonus(user_skills_lower: set[str], role_tags: list[str]) -> float:
    bonus = 0.0
    for skill in user_skills_lower:
        related = SKILL_GRAPH.get(skill, [])
        for rel in related:
            if rel in role_tags:
                bonus += 0.05
    return min(bonus, 0.3)


# ─── Main Recommendation Function ────────────────────────────────────────────

def get_recommendations(
    user_skills: list[str],
    top_n: int = 12,
    diversify: bool = False,
    strict: bool = False,
    category_filter: str | None = None,
) -> dict[str, Any]:
    t0 = time.perf_counter()
    roles = JOB_ROLES_DB
    if category_filter:
        roles = [r for r in roles if r["category"] == category_filter]

    idf = _build_idf(roles)
    user_skills_lower = [s.lower().strip() for s in user_skills]
    user_vec = _tfidf_vector(user_skills_lower, idf)

    results = []
    for role in roles:
        role_vec = _tfidf_vector(role["tags"], idf)
        cos_sim = _cosine(user_vec, role_vec)

        # strict mode: require at least 1 tag match
        matched_tags = [t for t in role["tags"] if t in user_skills_lower]
        if strict and not matched_tags:
            continue

        bm25 = _bm25_score(user_skills_lower, role["tags"], idf)
        graph_bonus = _skill_graph_bonus(set(user_skills_lower), role["tags"])

        # normalise bm25 to 0-1 range (heuristic max ~20)
        bm25_norm = min(bm25 / 20, 1.0)
        hybrid_score = 0.55 * cos_sim + 0.30 * bm25_norm + 0.15 * graph_bonus

        missing_tags = [t for t in role["tags"] if t not in user_skills_lower][:5]
        match_pct = round(hybrid_score * 100, 1)

        results.append({
            **role,
            "match_score": match_pct,
            "cosine_similarity": round(cos_sim, 4),
            "bm25_score": round(bm25, 4),
            "hybrid_score": round(hybrid_score, 4),
            "matched_tags": matched_tags,
            "missing_tags": missing_tags,
            "skill_gap": len(missing_tags),
            "coverage_pct": round(len(matched_tags) / len(role["tags"]) * 100, 1),
        })

    results.sort(key=lambda x: x["hybrid_score"], reverse=True)

    if diversify:
        results = _diversify(results, top_n)
    else:
        results = results[:top_n]

    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "recommendations": results,
        "meta": {
            "total_roles_searched": len(roles),
            "user_skills": user_skills_lower,
            "top_n": top_n,
            "diversify": diversify,
            "strict": strict,
            "elapsed_ms": elapsed,
            "algorithm": "Hybrid TF-IDF × BM25 × Skill-Graph (cosine)",
        },
    }


def _diversify(results: list[dict], top_n: int) -> list[dict]:
    """Ensure category diversity in top results."""
    seen_cats: dict[str, int] = {}
    out = []
    remainder = []
    for r in results:
        cat = r["category"]
        if seen_cats.get(cat, 0) < 3:
            out.append(r)
            seen_cats[cat] = seen_cats.get(cat, 0) + 1
        else:
            remainder.append(r)
        if len(out) >= top_n:
            break
    # fill remaining slots
    for r in remainder:
        if len(out) >= top_n:
            break
        out.append(r)
    return out


# ─── Explainability ──────────────────────────────────────────────────────────

def explain_recommendation(role: dict, user_skills: list[str]) -> dict:
    user_lower = [s.lower() for s in user_skills]
    matched = role.get("matched_tags", [])
    missing = role.get("missing_tags", [])

    # Weight matched skills by IDF-like rarity
    idf = _build_idf(JOB_ROLES_DB)
    weighted = sorted(matched, key=lambda t: idf.get(t, 1), reverse=True)

    # Learning path priority: rarest missing skills first
    priority_gaps = sorted(missing, key=lambda t: idf.get(t, 0), reverse=True)[:5]

    return {
        "role_id": role["id"],
        "role_title": role["title"],
        "match_score": role["match_score"],
        "top_matched_skills": weighted[:6],
        "skill_gap": priority_gaps,
        "coverage_pct": role.get("coverage_pct", 0),
        "match_reason": _build_reason(role, matched),
        "learning_path": _generate_learning_path(priority_gaps),
        "demand_level": _demand_label(role["demand"]),
        "salary_insight": _salary_insight(role),
    }


def _build_reason(role: dict, matched: list[str]) -> str:
    if not matched:
        return "Potential stretch role — no direct skill overlap detected."
    top = matched[:3]
    return (
        f"Strong alignment via {', '.join(top[:2])}"
        + (f" and {top[2]}" if len(top) > 2 else "")
        + f". Your profile covers {role.get('coverage_pct', 0):.0f}% of required skills."
    )


def _generate_learning_path(gaps: list[str]) -> list[dict]:
    resources: dict[str, dict] = {
        "python": {"url": "https://docs.python.org", "platform": "Official Docs", "hours": 40},
        "machine learning": {"url": "https://coursera.org/learn/machine-learning", "platform": "Coursera", "hours": 60},
        "deep learning": {"url": "https://fast.ai", "platform": "fast.ai", "hours": 80},
        "kubernetes": {"url": "https://kubernetes.io/docs/tutorials", "platform": "CNCF", "hours": 30},
        "aws": {"url": "https://aws.amazon.com/training", "platform": "AWS Training", "hours": 40},
        "docker": {"url": "https://docs.docker.com/get-started", "platform": "Docker Docs", "hours": 15},
        "react": {"url": "https://react.dev/learn", "platform": "React Docs", "hours": 30},
        "sql": {"url": "https://mode.com/sql-tutorial", "platform": "Mode Analytics", "hours": 20},
        "terraform": {"url": "https://developer.hashicorp.com/terraform/tutorials", "platform": "HashiCorp", "hours": 20},
        "pytorch": {"url": "https://pytorch.org/tutorials", "platform": "PyTorch Docs", "hours": 50},
        "nlp": {"url": "https://huggingface.co/course", "platform": "HuggingFace", "hours": 60},
        "llm": {"url": "https://learn.deeplearning.ai", "platform": "DeepLearning.AI", "hours": 40},
    }
    path = []
    for i, gap in enumerate(gaps[:5]):
        res = resources.get(gap, {"url": f"https://www.google.com/search?q=learn+{gap.replace(' ', '+')}", "platform": "Google", "hours": 20})
        path.append({
            "skill": gap,
            "priority": i + 1,
            "resource": res["url"],
            "platform": res["platform"],
            "estimated_hours": res["hours"],
        })
    return path


def _demand_label(demand: int) -> str:
    if demand >= 95: return "🔥 Extremely High"
    if demand >= 88: return "⚡ Very High"
    if demand >= 80: return "📈 High"
    if demand >= 70: return "➡️ Moderate"
    return "📉 Niche"


def _salary_insight(role: dict) -> str:
    mid = (role["salary_min"] + role["salary_max"]) / 2
    return (
        f"Market midpoint ~₹{mid:.0f} LPA. "
        f"Top performers reach ₹{role['salary_max']} LPA with 3-5 yrs experience."
    )


# ─── Analytics ───────────────────────────────────────────────────────────────

def compute_analytics(user_skills: list[str], recommendations: list[dict]) -> dict:
    if not recommendations:
        return {}

    scores = [r["match_score"] for r in recommendations]
    demands = [r["demand"] for r in recommendations]
    cats = {}
    for r in recommendations:
        cats[r["category"]] = cats.get(r["category"], 0) + 1

    salary_data = [
        {"title": r["title"][:20], "min": r["salary_min"], "max": r["salary_max"],
         "mid": (r["salary_min"] + r["salary_max"]) / 2}
        for r in recommendations
    ]

    # Skill frequency across recommended roles
    skill_freq: dict[str, int] = {}
    for r in recommendations:
        for tag in r["tags"]:
            skill_freq[tag] = skill_freq.get(tag, 0) + 1

    top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:15]

    # Gap analysis
    user_lower = set(s.lower() for s in user_skills)
    all_missing: dict[str, int] = {}
    for r in recommendations:
        for tag in r.get("missing_tags", []):
            if tag not in user_lower:
                all_missing[tag] = all_missing.get(tag, 0) + 1

    top_gaps = sorted(all_missing.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_roles": len(recommendations),
        "avg_match_score": round(sum(scores) / len(scores), 1),
        "max_match_score": max(scores),
        "min_match_score": min(scores),
        "avg_demand": round(sum(demands) / len(demands), 1),
        "category_distribution": cats,
        "salary_data": salary_data,
        "top_matched_skills": top_skills,
        "top_skill_gaps": top_gaps,
        "remote_friendly": sum(1 for r in recommendations if r.get("remote")),
        "high_growth": sum(1 for r in recommendations if int(r.get("growth", "0%").replace("+","").replace("%","")) >= 20),
        "match_distribution": {
            "excellent (>70%)": sum(1 for s in scores if s > 70),
            "good (50-70%)": sum(1 for s in scores if 50 <= s <= 70),
            "fair (30-50%)": sum(1 for s in scores if 30 <= s < 50),
            "stretch (<30%)": sum(1 for s in scores if s < 30),
        },
    }