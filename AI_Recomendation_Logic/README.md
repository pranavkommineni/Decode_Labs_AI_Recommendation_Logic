#  NeuralPath — AI Career Recommendation System

A professional full-stack AI Recommendation System with a stunning animated dashboard.

---

##  Quick Start

### Step 1 — Start the Backend (Python / FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- for frontend 
```bash
cd frontend
start index.html
```

- Backend runs at: **http://localhost:8000**
- Swagger API Docs: **http://localhost:8000/api/docs**


##  Project Structure

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

#  Project Overview

The **AI Career Recommendation Engine** is a smart career guidance platform that leverages advanced recommendation algorithms and skill intelligence to help users discover the most suitable technology career paths based on their existing skills, interests, and competencies.

This project combines multiple Artificial Intelligence and Information Retrieval techniques to provide highly accurate, personalized, and explainable career recommendations.

Unlike traditional recommendation systems that rely on static questionnaires and simple keyword matching, this system analyzes skill relationships, role compatibility, market demand, and user profiles to generate intelligent recommendations.

---


#  Key Features

##  Hybrid Recommendation Engine

The recommendation system combines:

### TF-IDF Vectorization
Evaluates the importance of skills across all career roles.

### Cosine Similarity
Measures similarity between user skills and job requirements.

### BM25 Ranking
Improves recommendation quality using information retrieval techniques.

### Skill Graph Intelligence
Detects hidden relationships between technical skills.

Example:

Machine Learning
├── Python
├── Statistics
├── Data Analysis
├── Deep Learning
└── TensorFlow

This allows the engine to recommend suitable careers even when users possess related skills instead of exact matches.

---

##  Personalized Career Recommendations

The system recommends roles such as:

- Machine Learning Engineer
- Data Scientist
- AI Engineer
- NLP Engineer
- Computer Vision Engineer
- Full Stack Developer
- Backend Developer
- Cloud Engineer
- DevOps Engineer
- Cybersecurity Analyst
- Blockchain Developer
- Software Engineer

and many more.

---

##  Explainable AI (XAI)

Each recommendation includes:

- Match Score
- Skill Coverage
- Missing Skills
- Matched Skills
- Recommendation Explanation
- Career Insights

Users can clearly understand why a recommendation was generated.

---

##  Analytics Dashboard

Provides:

- Recommendation Statistics
- Skill Gap Analysis
- Career Distribution
- Demand Analysis
- Growth Insights

---

##  FastAPI Backend

Features:

- High Performance APIs
- Automatic Documentation
- Type Validation
- Error Handling
- Easy Deployment

---

##  Interactive Frontend

Features:

- Modern Responsive UI
- Real-time Recommendations
- Dynamic Skill Selection
- Interactive Analytics
- User-Friendly Experience

---

#  System Architecture

```text
┌───────────────────────────┐
│         Frontend          │
│      HTML • CSS • JS      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      FastAPI Backend      │
│      RESTful Services     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Recommendation Engine     │
│                           │
│ • TF-IDF                  │
│ • Cosine Similarity       │
│ • BM25 Ranking            │
│ • Skill Intelligence      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Career Dataset        │
│                           │
│ • Roles                   │
│ • Skills                  │
│ • Demand Metrics          │
│ • Career Information      │
└───────────────────────────┘
```

---

#  Project Structure

```text
AI_Career_Recommendation_Engine/
│
├── backend/
│   │
│   ├── main.py
│   ├── recommendation_engine.py
│   ├── data.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── dataset/
│   │
│   └── careers.json
│
├── docs/
│
├── screenshots/
│
└── README.md
```

---

#  Technologies Used

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

## Frontend

- HTML5
- CSS3
- JavaScript

## AI & Recommendation

- TF-IDF
- Cosine Similarity
- BM25
- Skill Graph Intelligence

## Development Tools

- Git
- GitHub
- VS Code

---

#  Core Algorithms

## 1. TF-IDF

Calculates the importance of a skill across all career roles.

Formula:

TF-IDF = TF × IDF

Benefits:

- Identifies important skills
- Reduces common skill bias
- Improves recommendation quality

---

## 2. Cosine Similarity

Measures similarity between:

User Skill Vector

and

Career Skill Vector

Formula:

Cos(A,B) = A·B / ||A|| ||B||

Benefits:

- Accurate matching
- Vector-based similarity scoring
- Better ranking precision

---

## 3. BM25 Ranking

Advanced information retrieval algorithm used to:

- Improve recommendation ranking
- Prioritize relevant skills
- Reduce noise in matching

---

## 4. Skill Graph Intelligence

Creates relationships between technical skills.

Example:

AWS
├── Cloud Computing
├── Networking
├── Security
├── Docker
└── Kubernetes

Benefits:

- Hidden skill detection
- Better recommendations
- Context-aware matching

---

#  Dataset Information

The system currently contains:

### Career Roles

80+ Technology Roles

Including:

- Artificial Intelligence
- Data Science
- Machine Learning
- Cloud Computing
- Cybersecurity
- Software Development
- DevOps
- Blockchain
- Networking

---

### Technical Skills

100+ Skills

Examples:

- Python
- Java
- SQL
- TensorFlow
- PyTorch
- Docker
- Kubernetes
- AWS
- Linux
- React
- Machine Learning
- NLP
- Deep Learning

---

# 🔌 API Endpoints

## Health Check

GET /api/health

---

## Available Skills

GET /api/skills

---

## Available Roles

GET /api/roles

---

## Role Details

GET /api/roles/{role_id}

---

## Generate Recommendations

POST /api/recommend

Example Request:

```json
{
  "skills": [
    "python",
    "machine learning",
    "sql"
  ],
  "top_n": 10
}
```

---

## Recommendation Explanation

POST /api/explain

---

## Analytics

POST /api/analytics

---

#  Installation Guide

## Clone Repository

```bash
git clone https://github.com/yourusername/AI-Career-Recommendation-Engine.git

cd AI-Career-Recommendation-Engine
```

---

## Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Server:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## Run Frontend

Open:

```text
frontend/index.html
```

in any modern web browser.

---

#  Sample Recommendation Flow

### User Skills

```text
Python
Machine Learning
SQL
TensorFlow
```

↓

### Recommendation Engine

↓

### Top Recommendations

```text
1. Machine Learning Engineer
2. Data Scientist
3. AI Engineer
4. NLP Engineer
5. Computer Vision Engineer
```



### Explainable Insights

- Match Score
- Missing Skills
- Career Guidance
- Learning Roadmap

---

#  Security Features

✔ Input Validation

✔ API Request Validation

✔ Exception Handling

✔ Type Safety

✔ Secure Backend Architecture

✔ Error Management

✔ Data Integrity Protection

---

#  Future Enhancements

- Resume Parsing
- LinkedIn Profile Analysis
- Learning Path Generator
- Salary Prediction
- AI Career Mentor
- LLM-Based Career Advisor
- Certification Recommendations
- Job Market Integration
- Interview Preparation Module

---

#  Project Development 

## 🔹 [10 June 2026]
### Research & Planning Phase

- Identified project objectives
- Conducted requirement analysis
- Studied recommendation system architectures
- Selected FastAPI framework
- Designed overall system architecture
- Created initial career dataset structure

---

## 🔹 [11 June 2026]
### Backend Development

- Developed FastAPI backend
- Implemented API endpoints
- Added request validation using Pydantic
- Created modular backend architecture
- Built role and skill management modules


---

## 🔹 [12 June 2026]
### Recommendation Engine Development

- Implemented TF-IDF algorithm
- Developed Cosine Similarity calculations
- Integrated BM25 ranking mechanism
- Created recommendation scoring pipeline
- Optimized recommendation performance


---

## 🔹 [13 June 2026]
### Frontend & Intelligence Layer

- Built interactive frontend dashboard
- Added dynamic skill selection system
- Developed Skill Graph Intelligence
- Implemented Explainable AI module
- Connected frontend with backend APIs


---

## 🔹 [14 June 2026]
### Testing, Optimization & Documentation

- Conducted system testing
- Fixed bugs and performance issues
- Improved recommendation accuracy
- Finalized UI enhancements
- Prepared technical documentation
- Completed README and deployment setup


---

#  Author

## Kommineni Pranav

B.Tech Student | AI Enthusiast | Software Developer

Passionate about Artificial Intelligence, Machine Learning, Recommendation Systems, and Full Stack Development.

---

#  Project Outcome

The AI Career Recommendation Engine successfully demonstrates the application of Artificial Intelligence, Information Retrieval, and Explainable AI techniques to solve real-world career guidance challenges.

The project provides:

✅ Personalized Recommendations

✅ Explainable Results

✅ Skill Gap Analysis

✅ Career Insights

✅ Scalable Architecture

✅ Professional User Experience

This project serves as a strong demonstration of modern recommendation system design and practical AI application in career guidance.

---


