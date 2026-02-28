# System Architecture

## Overview

Instant Integrity MVP uses a cloud-native architecture with Next.js frontend, FastAPI backend, Supabase for authentication and persistence, and HuggingFace for AI-powered authenticity classification.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend (Next.js 14)"
        UI[Dashboard UI]
        SC[SpectralChart]
        CG[ConfidenceGauge]
        TT[ThemeToggle]
        AG[AuthGuard]
    end

    subgraph "Backend (FastAPI)"
        API[REST API]
        PP[Preprocessing Pipeline]
        HFC[HuggingFace Client]
        MW[Auth Middleware]
    end

    subgraph "Supabase Cloud"
        AUTH[Supabase Auth]
        DB[(PostgreSQL DB)]
    end

    subgraph "HuggingFace"
        ZSC[Zero-Shot Classification]
        MODEL[facebook/bart-large-mnli]
    end

    UI --> API
    SC --> API
    CG --> API
    AG --> AUTH
    API --> MW
    MW --> AUTH
    API --> PP
    PP --> HFC
    HFC --> ZSC
    ZSC --> MODEL
    API --> DB
```

## Component Details

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Next.js 14, React 18, TailwindCSS | Dashboard, charts, dark mode UI |
| Backend | FastAPI, Python 3.11+ | REST API, preprocessing, orchestration |
| Auth | Supabase Auth | User registration, login, JWT tokens |
| Database | Supabase PostgreSQL | Samples, results, user data |
| ML/AI | HuggingFace Inference API | Zero-shot classification for authenticity |
| Charts | Recharts | Spectral data visualization |

## Preprocessing Pipeline

```mermaid
graph LR
    CSV[CSV Upload] --> BC[Baseline Correction]
    BC --> SG[Savitzky-Golay Smoothing]
    SG --> SNV[SNV Normalization]
    SNV --> FT[Feature Text Generation]
    FT --> HF[HuggingFace Zero-Shot]
    HF --> RES[Classification Result]
```
