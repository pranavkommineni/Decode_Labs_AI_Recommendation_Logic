# 🧠 NeuralPath — AI Career Intelligence Dashboard

A professional full-stack AI Recommendation System with a stunning animated dashboard.

---

## 🚀 Quick Start

### Step 1 — Start the Backend (Python / FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the one-click script:
```bash
cd backend
bash run.sh
```

- Backend runs at: **http://localhost:8000**
- Swagger API Docs: **http://localhost:8000/api/docs**

### Step 2 — Add Your Data

Edit **`backend/data.py`** and fill in your:
- `JOB_ROLES_DB` — list of role objects
- `ALL_SKILLS` — list of skill strings
- `CATEGORIES` — auto-computed or manual list

Each role must include: `id`, `title`, `category`, `tags`, `demand`, `salary_min`, `salary_max`, `growth`, `remote`, `difficulty`, `description`, `certs`, `tools`.

### Step 3 — Open the Frontend

Open **`frontend/index.html`** in any modern browser.

> No build step required. Pure HTML/CSS/JS — zero dependencies.

---

## 📁 Project Structure

```
AI_CareerRec_Pro/
│
├── backend/
│   ├── main.py                # FastAPI app — all API routes
│   ├── recommendation_engine.py  # TF-IDF · BM25 · SkillGraph algorithms
│   ├── data.py                # YOUR dataset goes here (80 roles · 100+ skills)
│   ├── requirements.txt       # Python dependencies
│   └── run.sh                 # One-click start script
│
├── frontend/
│   └── index.html             # Complete dashboard (single-file, zero deps)
│
└── README.md
```

---

## ✨ Features

### 🎯 AI Recommendation Engine
- Hybrid **TF-IDF × BM25 × Skill Graph** scoring
- Cosine similarity vector matching
- **Diversify mode** — spread results across categories
- **Strict mode** — only high-coverage matches

### 📊 Dashboard
- 4 animated stat cards with live data from the API
- Real-time skill input with tag UI
- Score rings showing match % per role
- Color-coded matched / missing skill tags
- Animated progress bars

### 🔍 Explainable AI (XAI)
- Coverage % bar per role
- Matched vs missing skill breakdown
- Prioritised learning path with resource links
- Market insights (salary, demand)

### 🗺️ Explore Roles
- Browse all roles with search + filter + sort
- Click any card for detailed modal view

### ⚡ Skills Heatmap
- All skills as interactive heatmap cells
- Click to add to your profile instantly

### 📈 Analytics
- Category distribution bar charts
- Top skill gaps across matched roles
- Match quality distribution

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Global statistics |
| GET | `/api/skills` | All skills (filterable) |
| GET | `/api/roles` | All roles (filterable) |
| GET | `/api/roles/{id}` | Single role detail |
| GET | `/api/categories` | Categories with counts |
| POST | `/api/recommend` | Get AI recommendations |
| POST | `/api/explain` | XAI breakdown for a role |
| POST | `/api/analytics` | Analytics for a skill set |

---

## 💡 Demo Mode

If the backend isn't running, the dashboard automatically switches to **Demo Mode** with sample data so you can explore the UI without the server.

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | FastAPI (Python) |
| Algorithm | TF-IDF + BM25 + Skill Graph |
| Validation | Pydantic v2 |
| Server | Uvicorn (ASGI) |
| Frontend | Vanilla HTML/CSS/JS |
| Fonts | Google Fonts (Inter + JetBrains Mono) |
| Styling | CSS Variables + Animations |

---

Built with ❤️ for **Project 3: AI Recommendation Logic**
