---

# **📄 Technical Documentation – Phase 1**

**Project:** Instant Integrity MVP  
 **Phase:** Backend Skeleton & Project Setup

---

## **1\. Objective**

Establish a foundational backend environment with GitHub integration, containerization, and a minimal API that supports authentication and sample data upload. This phase sets the groundwork for later integration of chemometric models and advanced features.

---

## **2\. Scope**

* GitHub repository setup with CI/CD pipeline.  
* Backend skeleton using **FastAPI**.  
* Database setup with **PostgreSQL** and **Redis**.  
* Authentication via **JWT**.  
* One mock API endpoint for sample upload.  
* Dockerized environment with `docker-compose`.

---

## **3\. System Architecture (Phase 1\)**

\+------------------+        \+------------------+        \+------------------+  
|  Client (API)    | \-----\> |  FastAPI Backend | \-----\> | PostgreSQL DB    |  
| (curl/Postman)   |        |  (Dockerized)    |        | (Dockerized)     |  
\+------------------+        \+------------------+        \+------------------+  
         |                          |                          |  
         |                          |                          |  
         |                          v                          |  
         |                 \+------------------+                |  
         |                 | Redis Cache      |                |  
         |                 | (Dockerized)     |                |  
         |                 \+------------------+                |  
         |                          |                          |  
         v                          v                          v  
\+------------------+        \+------------------+        \+------------------+  
| GitHub Repo      | \-----\> | GitHub Actions   | \-----\> | Deployment Env   |  
| (Code \+ Issues)  |        | (CI/CD pipeline) |        | (Heroku/Render)  |  
\+------------------+        \+------------------+        \+------------------+

---

## **4\. Project Structure**

instant-integrity-mvp/  
│  
├── backend/  
│   ├── app/  
│   │   ├── main.py          \# FastAPI entrypoint  
│   │   ├── models/          \# SQLAlchemy models  
│   │   ├── schemas/         \# Pydantic schemas  
│   │   ├── routes/          \# API endpoints  
│   │   ├── services/        \# business logic  
│   │   └── core/            \# config, security, db connection  
│   ├── tests/  
│   │   ├── test\_auth.py  
│   │   └── test\_api.py  
│   ├── requirements.txt  
│   └── Dockerfile  
│  
├── docker-compose.yml  
├── README.md  
├── LICENSE  
└── .gitignore

---

## **5\. Dependencies**

* **FastAPI** – API framework.  
* **Uvicorn** – ASGI server.  
* **SQLAlchemy** – ORM for Postgres.  
* **Pydantic** – Data validation.  
* **psycopg2-binary** – Postgres driver.  
* **Redis** – Cache/session store.  
* **python-jose\[cryptography\]** – JWT handling.  
* **passlib\[bcrypt\]** – Password hashing.

---

## **6\. API Endpoints (Phase 1\)**

* `POST /auth/register` → Register new user.  
* `POST /auth/login` → Authenticate user, return JWT.  
* `POST /samples/upload` → Upload CSV spectral data, return mock authenticity result.

**Sample Response (mock):**

{  
  "status": "Authentic",  
  "confidence": 0.85  
}

---

## **7\. Dockerization**

**Dockerfile (backend):**

FROM python:3.11-slim  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install \-r requirements.txt  
COPY . .  
CMD \["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"\]

**docker-compose.yml:**

version: '3.8'  
services:  
  backend:  
    build: ./backend  
    ports:  
      \- "8000:8000"  
    depends\_on:  
      \- postgres  
      \- redis  
  postgres:  
    image: postgres:latest  
    environment:  
      POSTGRES\_USER: user  
      POSTGRES\_PASSWORD: password  
      POSTGRES\_DB: integrity  
    ports:  
      \- "5432:5432"  
  redis:  
    image: redis:latest  
    ports:  
      \- "6379:6379"

---

## **8\. CI/CD Pipeline**

* **GitHub Actions Workflow:**  
  * Trigger: Pull requests to `main`.  
  * Steps:  
    1. Install dependencies.  
    2. Run tests (`pytest`).  
    3. Build Docker image.  
    4. Deploy to Heroku/Render (optional in Phase 1).

---

## **9\. Deliverables**

* GitHub repo with README, LICENSE, `.gitignore`.  
* Backend skeleton with FastAPI.  
* JWT authentication implemented.  
* Mock sample upload endpoint.  
* Dockerized environment with Postgres \+ Redis.  
* CI/CD pipeline for testing.

---

## **10\. Next Steps (Phase 2 Preview)**

* Integrate **chemometric preprocessing** (noise reduction, PCA).  
* Train a simple classifier (authentic vs suspect).  
* Replace mock results with real model predictions.  
* Expand API to support batch-level analysis.

---

✅ This documentation now serves as your **Phase 1 technical reference**. It’s structured, complete, and ready to guide implementation.

Would you like me to also **draft the YouTrack epics \+ tasks for Phase 1** so you can paste them directly into your project board and start tracking progress?

# **Instant Integrity MVP technical documentation**

---

## **Overview and goals**

Instant Integrity is a proof-of-concept platform that delivers instant authenticity analysis using spectroscopy, chemometrics, and AI. The MVP demonstrates end-to-end flow from spectral data input to cloud-backed processing and clear decision outputs, while laying a scalable foundation for security, performance, and DevOps.

* Primary MVP goals:  
  * Accept spectral data uploads (CSV or device integration mock).  
  * Preprocess and analyze data to produce authenticity decisions.  
  * Provide a dashboard/API that returns results within seconds.  
  * Ensure basic security, observability, and CI/CD are in place.  
* Constraints:  
  * Zero-cost development; leverage free/open-source tooling and free tiers.  
  * Phased delivery: start lean, show scalability roadmap.  
* Target stack emphasis:  
  * Backend: Python \+ FastAPI, PostgreSQL, Redis, Docker.  
  * Frontend: Next.js \+ Tailwind (or Streamlit for the fastest PoC UI).  
  * DevOps: GitHub \+ Actions, containerization, optional Heroku/Render.  
  * Observability: Logging first, then Sentry; Prometheus/Grafana later phases.

---

## **Architecture summary**

### **High-level components**

* Data acquisition: Handheld/benchtop spectroscopy devices (mocked via CSV in MVP).  
* Processing and analysis:  
  * Phase 1: Validation \+ mock decision engine.  
  * Phase 2: Chemometric preprocessing \+ simple classifier.  
* Delivery:  
  * REST API (FastAPI).  
  * Dashboard (Next.js or Streamlit for PoC).  
* Persistence:  
  * PostgreSQL for users, samples, results.  
  * Redis for caching and short-lived state.  
* Security:  
  * JWT auth, hashed passwords, validated inputs.  
* DevOps:  
  * Docker, docker-compose, GitHub Actions CI.  
* Optional assistants:  
  * External AI assistants (free MCP servers) for non-sensitive coding tasks.

---

## **Phase plan and deliverables**

### **Phase 1: Backend skeleton and project setup**

* GitHub repository and branching strategy.  
* FastAPI app with JWT authentication.  
* PostgreSQL schema for users, samples, results.  
* Redis integration for caching (optional use in Phase 1).  
* CSV upload endpoint returning mock authenticity result.  
* Dockerization with docker-compose.  
* CI pipeline to run tests and build images.  
* Basic logging and optional Sentry.

### **Phase 2: Chemometric model integration**

* Preprocessing: baseline correction, noise reduction, normalization.  
* Feature extraction: PCA; optional PLS for extended analysis.  
* Simple classifier: logistic regression or one-class SVM for “authentic vs suspect.”  
* Model service and versioning; inference endpoint replacing mock.  
* Batch processing endpoints; confidence scoring and thresholds.  
* Enhanced dashboard visualization (spectra plots, PCA projections).

### **Phase 3: Frontend and supply chain workflow**

* Next.js \+ Tailwind application with protected routes.  
* Operator, QC Manager views; batch summaries and reports.  
* Role-based access control (extend JWT with roles).  
* Exportable CSV/PDF reports; audit logs.

### **Phase 4: Scaling and observability**

* Kubernetes (demo manifests), Nginx reverse proxy, horizontal scaling strategy.  
* Prometheus metrics, Grafana dashboards.  
* Sentry integrated across backend and frontend.  
* Performance testing: Playwright E2E, Lighthouse audits.  
* Resilience patterns: retries, backoff, circuit breakers (where relevant).

---

## **Detailed implementation specifications**

### **Repository structure**

instant-integrity-mvp/  
├── backend/  
│   ├── app/  
│   │   ├── main.py  
│   │   ├── core/            \# config, db, security, settings  
│   │   │   ├── config.py  
│   │   │   ├── database.py  
│   │   │   └── security.py  
│   │   ├── models/          \# SQLAlchemy models  
│   │   │   ├── user.py  
│   │   │   ├── sample.py  
│   │   │   └── result.py  
│   │   ├── schemas/         \# Pydantic schemas  
│   │   │   ├── auth.py  
│   │   │   ├── sample.py  
│   │   │   └── result.py  
│   │   ├── routes/          \# API endpoints  
│   │   │   ├── auth.py  
│   │   │   ├── samples.py  
│   │   │   └── results.py  
│   │   ├── services/        \# business logic  
│   │   │   ├── auth\_service.py  
│   │   │   └── analysis\_service.py  
│   │   ├── utils/           \# file parsing, validation  
│   │   │   └── csv\_parser.py  
│   │   └── ml/              \# Phase 2 models & preprocessing  
│   │       ├── preprocess.py  
│   │       ├── features.py  
│   │       ├── classifier.py  
│   │       └── model\_store.py  
│   ├── tests/  
│   │   ├── test\_auth.py  
│   │   ├── test\_samples.py  
│   │   └── test\_preprocess.py  
│   ├── requirements.txt  
│   ├── Dockerfile  
│   └── pyproject.toml       \# optional  
├── frontend/                \# Phase 3 (Next.js) or /dash (Streamlit PoC)  
│   └── (initialized later)  
├── docker-compose.yml  
├── .github/workflows/ci.yml  
├── .env.example  
├── README.md  
├── LICENSE  
└── .gitignore

### **Environment configuration**

* .env variables (never commit secrets):  
  * APP\_ENV=development  
  * DATABASE\_URL=postgresql://user:password@postgres:5432/integrity  
  * REDIS\_URL=redis://redis:6379/0  
  * JWT\_SECRET=change\_me  
  * JWT\_ALGORITHM=HS256  
  * SENTRY\_DSN=(optional)

### **Backend dependencies (backend/requirements.txt)**

fastapi  
uvicorn\[standard\]  
sqlalchemy  
psycopg2-binary  
alembic  
pydantic  
python-jose\[cryptography\]  
passlib\[bcrypt\]  
redis  
python-multipart  
numpy  
scipy  
scikit-learn  
matplotlib  
sentry-sdk

### **Database schema (SQLAlchemy models)**

#### **Users**

* id (UUID)  
* email (unique)  
* password\_hash (bcrypt)  
* role (enum: operator, manager, admin)  
* created\_at

#### **Samples**

* id (UUID)  
* user\_id (FK users.id)  
* filename  
* spectra\_points (JSON or separate table; MVP: JSON array)  
* metadata (JSON: sampling location, device, timestamp)  
* created\_at

#### **Results**

* id (UUID)  
* sample\_id (FK samples.id)  
* status (enum: authentic, suspect, verify)  
* confidence (float)  
* model\_version (string)  
* summary (text)  
* created\_at

### **JWT security and auth flow**

* Endpoints:  
  * POST /auth/register → email, password  
  * POST /auth/login → email, password → returns {access\_token, token\_type}  
* Middleware:  
  * Dependency to verify Authorization: Bearer \<token\> on protected routes.  
* Passwords hashed with bcrypt; minimum password policy.  
* Token payload includes: sub (user id), role, exp.

### **API endpoints (Phase 1\)**

#### **POST /samples/upload**

* Auth: required.  
* Input: multipart/form-data with file (CSV).  
* CSV format:  
  * Column headers: wavelength, absorbance  
  * Or single row vectors; parser normalizes into internal array structure.  
* Processing in Phase 1:  
  * Validate CSV structure and values.  
  * Store sample and raw data.  
  * Generate mock result:  
    * status \= “Authentic” or “Suspect” (random/heuristic placeholder).  
    * confidence \= 0.80–0.95 (placeholder).  
  * Persist result and return response.

Response example:

{  
  "sampleId": "c1b8f8bc-...",  
  "status": "Authentic",  
  "confidence": 0.87,  
  "modelVersion": "mock-v1",  
  "summary": "Phase 1 mock result. Analysis pending real model integration."  
}

#### **GET /results/{sample\_id}**

* Auth: required.  
* Returns the persisted result for a sample.  
* Includes summary and model version.

### **Dockerization**

#### **backend/Dockerfile**

FROM python:3.11-slim  
WORKDIR /app  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  
RUN apt-get update && apt-get install \-y build-essential && rm \-rf /var/lib/apt/lists/\*  
COPY requirements.txt .  
RUN pip install \--no-cache-dir \-r requirements.txt  
COPY . .  
CMD \["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"\]

#### **docker-compose.yml**

version: '3.8'  
services:  
  backend:  
    build: ./backend  
    environment:  
      \- APP\_ENV=development  
      \- DATABASE\_URL=postgresql://user:password@postgres:5432/integrity  
      \- REDIS\_URL=redis://redis:6379/0  
      \- JWT\_SECRET=change\_me  
      \- JWT\_ALGORITHM=HS256  
    ports:  
      \- "8000:8000"  
    depends\_on:  
      \- postgres  
      \- redis

  postgres:  
    image: postgres:15  
    environment:  
      POSTGRES\_USER: user  
      POSTGRES\_PASSWORD: password  
      POSTGRES\_DB: integrity  
    volumes:  
      \- pgdata:/var/lib/postgresql/data  
    ports:  
      \- "5432:5432"

  redis:  
    image: redis:7  
    ports:  
      \- "6379:6379"

volumes:  
  pgdata:

### **CI/CD: GitHub Actions (.github/workflows/ci.yml)**

name: CI

on:  
  pull\_request:  
    branches: \[ "main", "dev" \]  
  push:  
    branches: \[ "dev" \]

jobs:  
  build-and-test:  
    runs-on: ubuntu-latest  
    services:  
      postgres:  
        image: postgres:15  
        env:  
          POSTGRES\_USER: user  
          POSTGRES\_PASSWORD: password  
          POSTGRES\_DB: integrity\_test  
        ports:  
          \- 5432:5432  
        options: \>-  
          \--health-cmd="pg\_isready \-U user \-d integrity\_test"  
          \--health-interval=10s  
          \--health-timeout=5s  
          \--health-retries=5  
    steps:  
      \- uses: actions/checkout@v4  
      \- name: Set up Python  
        uses: actions/setup-python@v5  
        with:  
          python-version: '3.11'  
      \- name: Install dependencies  
        run: |  
          python \-m pip install \--upgrade pip  
          pip install \-r backend/requirements.txt  
      \- name: Run tests  
        working-directory: backend  
        env:  
          DATABASE\_URL: postgresql://user:password@localhost:5432/integrity\_test  
        run: |  
          pytest \-q

### **Logging and error tracking**

* Python logging configured at INFO level; JSON formatter optional.  
* Sentry SDK optional; configure via SENTRY\_DSN to capture exceptions.  
* Avoid leaking stack traces in API responses.

### **Unit and integration tests**

* test\_auth.py  
  * Register, login, token decode, protected route access.  
* test\_samples.py  
  * Upload valid CSV, invalid CSV, missing auth.  
* test\_preprocess.py (Phase 2\)  
  * Baseline correction behavior, PCA dimensions, classifier sanity.

---

## **Phase 2: chemometric and AI integration**

### **Preprocessing pipeline (app/ml/preprocess.py)**

* Baseline correction:  
  * Polynomial fitting or asymmetric least squares (ALS).  
* Noise reduction:  
  * Savitzky–Golay filter for smoothing.  
* Scatter correction / normalization:  
  * Standard normal variate (SNV) or mean-centering.  
* Spectral windowing:  
  * Optionally select relevant wavelength ranges.

### **Feature extraction (app/ml/features.py)**

* PCA:  
  * Fit PCA on training set (retain components explaining 95% variance).  
  * Transform incoming spectra for inference.  
* Optional PLS:  
  * PLS-DA for supervised class separation if label data available.

### **Classifier (app/ml/classifier.py)**

* Options:  
  * One-class SVM trained on authentic samples (detect outliers).  
  * Logistic regression or random forest when adulterated labels exist.  
* Thresholds:  
  * Confidence score calibrated via validation set; configurable thresholds for:  
    * Authentic  
    * Suspect  
    * Verify (send-to-lab)

### **Model storage and versioning (app/ml/model\_store.py)**

* Save fitted models (PCA, classifier) as joblib files in /models.  
* Maintain metadata:  
  * model\_version  
  * training\_date  
  * training\_data\_summary

### **Training script (scripts/train\_model.py)**

* Load dataset (open-source or curated).  
* Apply preprocessing, fit PCA, fit classifier.  
* Persist artifacts and metadata.  
* Output evaluation metrics (accuracy, ROC-AUC, confusion matrix).

### **Inference endpoint (Phase 2\)**

* POST /analysis/infer  
  * Auth: required.  
  * Input: CSV file or spectra array.  
  * Steps:  
    * Parse spectra → preprocess → transform → predict.  
    * Compute confidence and decision class.  
    * Persist result with modelVersion and summary.

Response:  
 {  
  "status": "Suspect",  
  "confidence": 0.72,  
  "modelVersion": "pca-ocs-1.0.0",  
  "explanations": {  
    "principalComponents": \[0.23, \-0.14, 0.07\],  
    "distanceToAuthenticManifold": 1.85  
  }  
}

* 

### **Visualization for dashboard**

* Spectra plot (raw vs. preprocessed).  
* PCA scatter: sample projection vs. authentic cluster.  
* Confidence bar and decision thresholds.

---

## **Phase 3: frontend and workflow**

### **Next.js \+ Tailwind setup**

* Pages:  
  * /login, /register  
  * /upload (protected)  
  * /results/:id  
  * /dashboard (manager view)  
* State and data fetching:  
  * React Query for API calls and caching.  
  * Zustand for lightweight global UI state.  
* Security:  
  * Store JWT securely; attach to Authorization headers.  
* Components:  
  * FileUploader, SpectraPlot (using Plotly or Chart.js), ResultCard, PCAPlot.

### **Storybook (optional)**

* Document UI components for reuse and team onboarding.

### **Playwright E2E (optional)**

* Tests for login, upload, and result view flows.

### **Lighthouse (optional)**

* Performance audits; ensure accessible and fast dashboard.

---

## **Phase 4: scaling and observability**

### **Kubernetes manifests (demo)**

* Deployments and Services for backend, Redis, Postgres (statefulset for prod).  
* Nginx ingress controller; TLS termination.  
* HorizontalPodAutoscaler (HPA) based on CPU/memory.

### **Observability**

* Prometheus:  
  * Exporter for Python metrics (prometheus-client).  
  * Custom metrics: request latency, inference time, upload counts.  
* Grafana:  
  * Dashboards for API performance, error rates, inference throughput.  
* Sentry:  
  * DSN in env; release tracking tied to Git SHA.

---

## **Security considerations**

### **Purpose**

* Preserve data integrity, trust, and reliability from MVP onward.  
* Demonstrate responsible handling of user data and results.

### **Scanning workflow**

* Authentication required before cloud upload and analysis.  
* Each scan linked to user account; audit trail preserved.  
* Optional guest mode for demo-only results (not persisted).

### **Security layers**

* API:  
  * JWT on protected routes.  
  * Input validation via Pydantic.  
  * CORS restricted to known frontends.  
* Database:  
  * Bcrypt hashed passwords.  
  * Principle of least privilege for DB user.  
* Infrastructure:  
  * Secrets via environment; no hardcoded credentials.  
  * Minimal port exposure; containers isolated by network.  
* Error handling:  
  * Avoid leaking stack traces; log exceptions; optional Sentry capture.

### **Roadmap**

* Role-based access control, encryption at rest, secret managers.  
* Audit logs and compliance support (GDPR, ISO).  
* Rate-limiting and abuse prevention.

---

## **External AI assistants (MCP servers) usage**

### **Rationale**

* Offload non-sensitive tasks (boilerplate code, documentation, tests) to free AI endpoints.  
* Maintain proprietary data (spectra, models) within controlled environment.

### **Integration points**

* IntelliJ agents query MCP servers for code scaffolding and refactoring suggestions.  
* Human review mandatory; commits linked to GitHub issues and PRs.  
* No sensitive payloads sent to external services.

### **Fallbacks and reliability**

* Local templates and snippets in repository for offline work.  
* Cached responses or recorded patterns to reduce repeated calls.

### **Policy**

* Document acceptable use:  
  * Allowed: utility functions, controller scaffolds, unit test templates.  
  * Not allowed: uploading sample data, model artifacts, or internal secrets.

---

## **GitHub project setup**

### **Repository initialization**

* README.md: vision, architecture diagram, phase roadmap.  
* LICENSE: MIT (recommended).  
* .gitignore: Python, Node, Docker entries.  
* Branches:  
  * main: reviewed and stable.  
  * dev: integration branch.  
  * feature/\*: per-task branches (e.g., feature/auth, feature/upload).

### **Issue templates**

* .github/ISSUE\_TEMPLATE/feature.md  
* .github/ISSUE\_TEMPLATE/bug.md

### **PR template**

* .github/pull\_request\_template.md

### **Labels and milestones**

* Labels: backend, frontend, devops, security, phase1, phase2, bug, docs.  
* Milestones: Phase 1, Phase 2, Phase 3\.

---

## **Developer workflow**

1. Create issue in GitHub for a task (e.g., “Implement JWT auth”).  
2. Create feature branch, link to issue.  
3. Use IntelliJ \+ agents to scaffold code; adhere to specs.  
4. Push branch; open PR; CI runs tests.  
5. Review and merge to dev; promote to main after validation.  
6. Tag release; optionally deploy to free-tier host.

---

## **Sample code snippets**

### **app/core/config.py**

from pydantic import BaseSettings

class Settings(BaseSettings):  
    app\_env: str \= "development"  
    database\_url: str  
    redis\_url: str  
    jwt\_secret: str  
    jwt\_algorithm: str \= "HS256"  
    sentry\_dsn: str | None \= None

    class Config:  
        env\_file \= ".env"

settings \= Settings()

### **app/core/security.py**

from datetime import datetime, timedelta  
from jose import jwt  
from passlib.context import CryptContext

pwd\_context \= CryptContext(schemes=\["bcrypt"\], deprecated="auto")

def hash\_password(password: str) \-\> str:  
    return pwd\_context.hash(password)

def verify\_password(password: str, hashed: str) \-\> bool:  
    return pwd\_context.verify(password, hashed)

def create\_access\_token(sub: str, role: str, secret: str, algorithm: str, expires\_minutes: int \= 60):  
    payload \= {  
        "sub": sub,  
        "role": role,  
        "exp": datetime.utcnow() \+ timedelta(minutes=expires\_minutes)  
    }  
    return jwt.encode(payload, secret, algorithm=algorithm)

### **app/main.py**

from fastapi import FastAPI  
from app.routes import auth, samples, results

app \= FastAPI(title="Instant Integrity MVP")

app.include\_router(auth.router, prefix="/auth", tags=\["auth"\])  
app.include\_router(samples.router, prefix="/samples", tags=\["samples"\])  
app.include\_router(results.router, prefix="/results", tags=\["results"\])

### **app/routes/auth.py**

from fastapi import APIRouter, Depends, HTTPException  
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse  
from app.services.auth\_service import register\_user, authenticate\_user

router \= APIRouter()

@router.post("/register", response\_model=TokenResponse)  
def register(payload: RegisterRequest):  
    user, token \= register\_user(payload)  
    return TokenResponse(access\_token=token, token\_type="bearer")

@router.post("/login", response\_model=TokenResponse)  
def login(payload: LoginRequest):  
    token \= authenticate\_user(payload)  
    if not token:  
        raise HTTPException(status\_code=401, detail="Invalid credentials")  
    return TokenResponse(access\_token=token, token\_type="bearer")

### **app/routes/samples.py**

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException  
from app.schemas.sample import UploadResponse  
from app.services.analysis\_service import save\_sample\_and\_mock\_result  
from app.services.auth\_service import get\_current\_user

router \= APIRouter()

@router.post("/upload", response\_model=UploadResponse)  
async def upload\_sample(  
    file: UploadFile \= File(...),  
    user=Depends(get\_current\_user)  
):  
    if file.content\_type not in ("text/csv", "application/vnd.ms-excel"):  
        raise HTTPException(status\_code=400, detail="CSV required")  
    return await save\_sample\_and\_mock\_result(file, user.id)

---

## **MVP architecture diagram (data flow)**

\[Spectroscopy Device / CSV Upload\]  
                |  
        (Authenticated via JWT)  
                v  
        \[FastAPI Ingress Layer\]  
                |  
        Input validation (Pydantic)  
                |  
                v  
      \[Storage & Caching Layer\]  
   (PostgreSQL: users, samples, results)  
           (Redis: cache/session)  
                |  
                v  
      \[Analysis Service Layer\]  
   Phase 1: mock decision engine  
   Phase 2: preprocess \+ PCA \+ classifier  
                |  
                v  
         \[Result Generation\]  
   (status, confidence, modelVersion)  
                |  
                v  
       \[UI/Dashboard / API Client\]  
   (Next.js or Streamlit; reports and batch views)

---

## **Risk register and mitigations**

* Data sensitivity:  
  * Mitigation: authentication, audit logging, no persistence for guest mode.  
* Model reliability (Phase 2):  
  * Mitigation: clear thresholds, transparent confidence, “verify” path.  
* Free-tier limits:  
  * Mitigation: local docker-compose; avoid heavy workloads in hosted demos.  
* External AI assistants:  
  * Mitigation: policy restricting sensitive data; human review before merge.

---

## **Acceptance criteria (Phase 1\)**

* API responds on /auth and /samples/upload.  
* Protected routes require JWT; invalid tokens rejected.  
* CSV upload persists sample and returns mock decision.  
* Docker-compose starts backend, Postgres, Redis; health verified.  
* CI passes: unit tests for auth and upload succeed.

---

If you confirm Phase 1 documentation is complete and usable, I’ll proceed to draft Phase 2 technical documentation with detailed preprocessing steps, model training script, inference endpoints, and visualization guidance.

