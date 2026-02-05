# API Contracts Summary

**Feature**: Phase 1 Backend Skeleton  
**Date**: 2025-11-23  
**Base URL**: `http://localhost:8000/api/v1`

## Overview

This document summarizes all REST API endpoints for Phase 1. Full OpenAPI specifications are available in individual contract files.

---

## Authentication Endpoints

### POST /auth/register

**Purpose**: Create new user account

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (201 Created):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 400: Invalid email format or password too short
- 409: Email already registered

---

### POST /auth/login

**Purpose**: Authenticate existing user

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 400: Invalid request format
- 401: Invalid credentials

---

## Sample Endpoints

### POST /samples/upload

**Purpose**: Upload CSV spectral data for analysis

**Authentication**: Required (JWT Bearer token)

**Request**: Multipart form-data
- `file`: CSV file (max 10MB)

**CSV Format**:
```csv
wavelength,absorbance
400.0,0.123
401.0,0.125
...
```

**Success Response** (201 Created):
```json
{
  "sample_id": "f1e2d3c4-b5a6-4789-9012-3456789abcde",
  "status": "Authentic",
  "confidence": 0.87,
  "model_version": "mock-v1.0",
  "summary": "Phase 1 mock result. Real analysis in Phase 2."
}
```

**Error Responses**:
- 400: Invalid CSV format or file too large
- 401: Missing or invalid authentication token
- 413: File size exceeds 10MB limit

---

## Result Endpoints

### GET /results/{sample_id}

**Purpose**: Retrieve analysis result for a sample

**Authentication**: Required (JWT Bearer token)

**Path Parameters**:
- `sample_id`: UUID of the sample

**Success Response** (200 OK):
```json
{
  "id": "e1f2g3h4-i5j6-4789-9012-3456789abcde",
  "sample_id": "f1e2d3c4-b5a6-4789-9012-3456789abcde",
  "status": "Authentic",
  "confidence": 0.87,
  "model_version": "mock-v1.0",
  "summary": "Phase 1 mock result. Real analysis in Phase 2.",
  "created_at": "2025-11-23T16:45:01Z"
}
```

**Error Responses**:
- 401: Missing or invalid authentication token
- 403: Unauthorized (sample belongs to another user)
- 404: Sample not found

---

## Health Check Endpoint

### GET /health

**Purpose**: Service health check for monitoring

**Authentication**: Not required

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2025-11-23T16:40:00Z"
}
```

---

## Common Response Formats

### Error Response

All error responses follow this format:

```json
{
  "status_code": 400,
  "message": "Brief error description",
  "detail": "Detailed error information (optional)"
}
```

### Authentication Header

Protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists (e.g., duplicate email) |
| 413 | Payload Too Large | File upload exceeds size limit |
| 422 | Unprocessable Entity | Validation error (Pydantic) |
| 500 | Internal Server Error | Unexpected server error |

---

## Request/Response Examples

### Full Registration Flow

**1. Register New User**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhMWIyYzNkNC1lNWY2LTQ3ODktOTAxMi0zNDU2Nzg5YWJjZGUiLCJyb2xlIjoidXNlciIsImV4cCI6MTczMjM4NzIwMH0.xyz",
  "token_type": "bearer"
}
```

**2. Upload Sample**
```bash
curl -X POST http://localhost:8000/api/v1/samples/upload \
  -H "Authorization: Bearer eyJhbGci..." \
  -F "file=@sample_flour.csv"
```

Response:
```json
{
  "sample_id": "f1e2d3c4-b5a6-4789-9012-3456789abcde",
  "status": "Authentic",
  "confidence": 0.87,
  "model_version": "mock-v1.0",
  "summary": "Phase 1 mock result. Real analysis in Phase 2."
}
```

**3. Retrieve Result**
```bash
curl -X GET http://localhost:8000/api/v1/results/f1e2d3c4-b5a6-4789-9012-3456789abcde \
  -H "Authorization: Bearer eyJhbGci..."
```

Response:
```json
{
  "id": "e1f2g3h4-i5j6-4789-9012-3456789abcde",
  "sample_id": "f1e2d3c4-b5a6-4789-9012-3456789abcde",
  "status": "Authentic",
  "confidence": 0.87,
  "model_version": "mock-v1.0",
  "summary": "Phase 1 mock result. Real analysis in Phase 2.",
  "created_at": "2025-11-23T16:45:01Z"
}
```

---

## Rate Limiting (Future - Phase 2)

Phase 1 has no rate limiting. Future phases will implement:
- **Authentication**: 5 requests/minute per IP
- **Uploads**: 10 requests/hour per user
- **General API**: 100 requests/minute per user

---

## API Versioning

- **Current Version**: v1
- **Base Path**: `/api/v1`
- **Future**: Breaking changes will increment version (`/api/v2`)
- **Deprecation**: Old versions supported for 6 months after new version release

---

## OpenAPI Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

**API Contracts Complete** - See individual contract files for full OpenAPI 3.0 specifications
