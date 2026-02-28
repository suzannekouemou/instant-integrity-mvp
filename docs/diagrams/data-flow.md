# Data Flow

## Overview

How spectral data flows from CSV upload through preprocessing, classification, storage, and visualization.

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph "Input"
        CSV[CSV File<br/>wavelength, absorbance]
    end

    subgraph "Preprocessing (Backend)"
        BC[Baseline Correction<br/>polynomial fitting]
        SG[Savitzky-Golay<br/>smoothing filter]
        SNV[SNV Normalization<br/>mean-center + scale]
        FT[Feature Text<br/>generation]
    end

    subgraph "Classification"
        HF[HuggingFace API<br/>Zero-Shot]
        LABELS[Candidate Labels<br/>authentic, adulterated,<br/>contaminated, degraded]
    end

    subgraph "Storage (Supabase)"
        DB[(PostgreSQL<br/>samples + results)]
    end

    subgraph "Presentation (Frontend)"
        CHART[SpectralChart<br/>recharts LineChart]
        GAUGE[ConfidenceGauge<br/>SVG circular gauge]
        BADGE[StatusBadge<br/>authentic / suspect]
    end

    CSV --> BC --> SG --> SNV --> FT
    FT --> HF
    LABELS --> HF
    HF --> DB
    DB --> CHART
    DB --> GAUGE
    DB --> BADGE
```

## Data Transformations

```mermaid
graph TD
    RAW[Raw Spectral Data<br/>wavelength + absorbance arrays] -->|Baseline Correction| T1[Corrected Spectrum<br/>polynomial baseline removed]
    T1 -->|Savitzky-Golay Filter| T2[Smoothed Spectrum<br/>noise reduced, derivatives preserved]
    T2 -->|SNV Normalization| T3[Normalized Spectrum<br/>mean=0, std=1 per sample]
    T3 -->|Feature Extraction| T4[Feature Text String<br/>spectral characteristics described]
    T4 -->|Zero-Shot Classification| T5[Prediction Result<br/>label + confidence score]
    T5 -->|Store| T6[Database Record<br/>sample_id, result, confidence, metadata]
```

## Data Schema

| Entity | Key Fields | Source |
|--------|-----------|--------|
| Sample | id, user_id, file_path, sample_type, created_at | CSV upload |
| Result | id, sample_id, prediction, confidence, status | HuggingFace API |
| User | id, email, created_at | Supabase Auth |
