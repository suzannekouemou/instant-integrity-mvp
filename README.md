# Instant Integrity MVP

## Overview

Instant Integrity is a cloud-powered authenticity verification platform that combines **spectroscopy, chemometrics, and AI** to deliver instant, reliable quality control across the supply chain — reducing fraud, saving costs, and raising global standards.

## Vision

A proof-of-concept platform that delivers instant authenticity analysis using spectroscopy data processed through chemometric models, delivered via the cloud for industries like food, herbs, spices, and flour.

## Key Features

- **Data Acquisition**: Integration with handheld and benchtop spectroscopy devices (FTIR, NIR)
- **Cloud-Based Chemometric Analysis**: Noise reduction, Savitzky-Golay smoothing, SNV normalization, AI-powered authenticity predictions
- **Decision Support**: Instant results (seconds), batch-level screening, clear authenticity indicators
- **Supply Chain Integration**: End-to-end visibility, cloud accessibility
- **Dark Mode UI**: Full light/dark theme support with system preference detection

## Technology Stack

### Frontend
- **Next.js 14** with React 18
- **TailwindCSS** with dark mode (`class` strategy)
- **Recharts** for spectral data visualization
- **Lucide React** for iconography

### Backend
- **Python 3.11+** with FastAPI
- **Supabase** for PostgreSQL database and authentication
- **Pydantic** for data validation

### ML / AI
- **HuggingFace Inference API** for zero-shot classification (`facebook/bart-large-mnli`)
- **NumPy, SciPy** for spectral preprocessing (baseline correction, Savitzky-Golay, SNV)

### Infrastructure
- **Supabase Cloud** for auth + database
- **GitHub Actions** for CI/CD

## Architecture

```
Next.js 14 Frontend
    ├── Dashboard (stats, recent results)
    ├── SpectralChart (recharts)
    ├── ConfidenceGauge (SVG)
    └── ThemeToggle (dark/light/system)
         │
         ▼
FastAPI Backend
    ├── Auth Middleware → Supabase Auth
    ├── Preprocessing Pipeline
    │   ├── Baseline Correction
    │   ├── Savitzky-Golay Smoothing
    │   └── SNV Normalization
    └── HuggingFace Client → Zero-Shot Classification
         │
         ▼
Supabase Cloud
    ├── PostgreSQL (samples, results, users)
    └── Auth (registration, login, JWT)
```

See [Architecture Diagrams](docs/diagrams/) for detailed Mermaid diagrams.

## Getting Started

### Prerequisites
- **Node.js 18+** and npm (frontend)
- **Python 3.11+** (backend)
- **Supabase account** (free tier works)
- **HuggingFace API token** (free tier works)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Supabase and HuggingFace credentials

# Run tests (30 tests expected)
python -m pytest

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Start development server
npm run dev

# Production build
npm run build
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | Yes |
| `HUGGINGFACE_API_KEY` | HuggingFace API token | Yes |

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` — Register new user via Supabase
- `POST /api/v1/auth/login` — Login and receive session token

### Samples (Authenticated)
- `POST /api/v1/samples/upload` — Upload CSV spectral data
  - Requires: auth token, CSV file, sample_type (flour/spice/herb/other)
  - Returns: authenticity prediction with confidence score

### Results (Authenticated)
- `GET /api/v1/results/{sample_id}` — Retrieve analysis result

### System
- `GET /health` — Health check
- `GET /docs` — Interactive API documentation (Swagger UI)

## Testing

```bash
# Backend tests (30 tests)
cd backend
source venv/bin/activate
python -m pytest

# With coverage
python -m pytest --cov=app --cov-report=term-missing

# Frontend build check
cd frontend
npm run build
```

## Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Backend skeleton, API, project setup |
| Phase 2 | ✅ Complete | Chemometric models, HuggingFace integration, preprocessing pipeline |
| Phase 3 | ✅ Complete | Next.js frontend, dashboard, dark mode, spectral charts, confidence gauge |
| Phase 4 | Planned | Scaling, observability, deployment |

## UI Components

| Component | File | Purpose |
|-----------|------|---------|
| SpectralChart | `frontend/src/components/SpectralChart.tsx` | Recharts-based spectral data visualization |
| ConfidenceGauge | `frontend/src/components/ConfidenceGauge.tsx` | SVG circular confidence indicator |
| ThemeProvider | `frontend/src/components/ThemeProvider.tsx` | Dark/light/system theme context |
| ThemeToggle | `frontend/src/components/ThemeToggle.tsx` | Sun/Moon/Monitor theme switcher |
| Dashboard | `frontend/src/app/dashboard/page.tsx` | Stats overview, recent results, upload CTA |

## Documentation

- [Architecture Diagrams](docs/diagrams/) — System architecture, user flow, data flow (Mermaid)
- [Design System](frontend/DESIGN_SYSTEM.md) — Colors, typography, components, accessibility
- [Constitution](.specify/memory/constitution.md) — Core principles and governance
- [Proof of Concept](Proof%20of%20Concept%20Document.md) — Project vision and architecture

## License

MIT License — See LICENSE file for details.

---

**Status**: ✅ Phase 3 Complete  
**Last Updated**: 2026-02-28  
**Next Phase**: Phase 4 — Scaling & Observability
