# User Flow

## Overview

End-to-end user journey from registration through sample analysis to results review.

## User Flow Diagram

```mermaid
flowchart TD
    START([User Visits App]) --> LOGIN{Authenticated?}

    LOGIN -->|No| REG[Register / Login via Supabase]
    REG --> AUTH[Supabase Auth Validates]
    AUTH --> TOKEN[JWT Token Issued]
    TOKEN --> DASH

    LOGIN -->|Yes| DASH[Dashboard]

    DASH --> STATS[View Stats Overview]
    DASH --> UPLOAD[Upload Spectral Data]
    DASH --> RESULTS[View Past Results]

    UPLOAD --> CSV[Select CSV File]
    CSV --> TYPE[Choose Sample Type]
    TYPE -->|flour / spice / herb / other| SUBMIT[Submit for Analysis]

    SUBMIT --> PREPROCESS[Backend Preprocesses Data]
    PREPROCESS --> CLASSIFY[HuggingFace Classification]
    CLASSIFY --> STORE[Store Result in Supabase DB]
    STORE --> DISPLAY[Display Result]

    DISPLAY --> CHART[View Spectral Chart]
    DISPLAY --> GAUGE[View Confidence Gauge]
    DISPLAY --> STATUS[View Authenticity Status]

    STATUS --> AUTHENTIC[Authentic - Green]
    STATUS --> SUSPECT[Suspect - Red]
    STATUS --> INCONCLUSIVE[Inconclusive - Yellow]

    RESULTS --> LIST[Browse Results List]
    LIST --> DETAIL[View Result Detail]
    DETAIL --> CHART
    DETAIL --> GAUGE
```

## Flow Summary

| Step | Action | Component |
|------|--------|-----------|
| 1 | Register or login | Supabase Auth |
| 2 | View dashboard stats | Dashboard page |
| 3 | Upload CSV spectral data | Upload form |
| 4 | Select sample type | Type selector |
| 5 | Backend preprocesses data | Preprocessing pipeline |
| 6 | AI classifies authenticity | HuggingFace API |
| 7 | View results with charts | SpectralChart + ConfidenceGauge |
| 8 | Review past analyses | Results list |
